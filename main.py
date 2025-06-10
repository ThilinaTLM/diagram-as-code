from diagrams import Diagram as _Diagram   
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import io
import os
import tempfile
import sys
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

app = FastAPI(title="Graph as Code Online", description="Generate diagrams from Python code")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5000",
        "http://0.0.0.0:5000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files from Vite build
static_dir = Path(__file__).parent / "web" / "dist"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

class DiagramWrapper:
    """Wrapper for Diagram that automatically injects filename and show parameters"""
    def __init__(self, name="", **kwargs):
        # Get the diagram_path from the calling context
        frame = sys._getframe(1)
        diagram_path = frame.f_globals.get('diagram_path', '/tmp/diagram')
        
        # Force the filename and show parameters
        kwargs['filename'] = diagram_path
        kwargs['show'] = False
        
        self._diagram = _Diagram(name, **kwargs)
    
    def __enter__(self):
        return self._diagram.__enter__()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._diagram.__exit__(exc_type, exc_val, exc_tb)
    
    def __getattr__(self, name):
        return getattr(self._diagram, name)

class DiagramsModuleWrapper:
    """Wrapper for the diagrams module that replaces Diagram with DiagramWrapper"""
    def __init__(self, original_module, diagram_wrapper_class):
        self._original_module = original_module
        self._diagram_wrapper_class = diagram_wrapper_class
    
    def __getattr__(self, name):
        if name == 'Diagram':
            return self._diagram_wrapper_class
        return getattr(self._original_module, name)

def execute_diagram_code(code):
    """Execute Python code to generate a diagram and return as BytesIO object"""
    with tempfile.TemporaryDirectory() as temp_dir:
        diagram_path = os.path.join(temp_dir, "diagram")
        
        # Import all the diagrams modules that might be used
        import diagrams
        import diagrams.aws.compute
        import diagrams.aws.database
        import diagrams.aws.network
        import diagrams.aws.storage
        import diagrams.aws.management
        import diagrams.onprem.client
        import diagrams.onprem.database
        import diagrams.onprem.network
        import diagrams.k8s.compute
        import diagrams.k8s.network
        import diagrams.k8s.storage
        
        # Create a wrapper for the diagrams module that replaces Diagram
        diagrams_wrapper = DiagramsModuleWrapper(diagrams, DiagramWrapper)
        
        # Store original diagrams module
        original_diagrams_module = sys.modules.get('diagrams')
        
        # Create execution environment with standard builtins but override Diagram
        safe_globals = {
            '__builtins__': __builtins__,
            'Diagram': DiagramWrapper,
            'Cluster': diagrams.Cluster,
            'diagrams': diagrams_wrapper,
            'diagram_path': diagram_path,
        }
        
        safe_locals = {}
        
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            # Temporarily replace the diagrams module in sys.modules
            sys.modules['diagrams'] = diagrams_wrapper
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals, safe_locals)
            
            # Look for generated PNG file
            png_file = diagram_path + ".png"
            if os.path.exists(png_file):
                with open(png_file, 'rb') as f:
                    img_data = io.BytesIO(f.read())
                    img_data.seek(0)
                    return img_data, None
            else:
                return None, "No diagram file was generated. Make sure your code creates a Diagram."
                
        except Exception as e:
            error_msg = f"Error executing code: {str(e)}"
            stderr_output = stderr_capture.getvalue()
            if stderr_output:
                error_msg += f"\nStderr: {stderr_output}"
            return None, error_msg
        finally:
            # Restore original diagrams module
            if original_diagrams_module:
                sys.modules['diagrams'] = original_diagrams_module

@app.post('/api/diagram')
async def execute_diagram(request: Request):
    """Execute Python code to generate a diagram"""
    try:
        # Handle both JSON and raw text input
        content_type = request.headers.get('content-type', '')
        
        if 'application/json' in content_type:
            data = await request.json()
            code = data.get('code')
            if not code:
                raise HTTPException(status_code=400, detail='No code provided in JSON body')
        else:
            # Accept raw text as Python code
            body = await request.body()
            code = body.decode('utf-8')
            if not code:
                raise HTTPException(status_code=400, detail='No code provided')
        
        # Execute the code and generate diagram
        img_data, error = execute_diagram_code(code)
        
        if error:
            raise HTTPException(status_code=400, detail=error)
        
        if img_data:
            return StreamingResponse(
                io.BytesIO(img_data.getvalue()),
                media_type='image/png',
                headers={'Content-Disposition': 'inline; filename=executed_diagram.png'}
            )
        else:
            raise HTTPException(status_code=400, detail='No diagram was generated')
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to execute code: {str(e)}')

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve the SPA for all non-API routes"""
    # Skip API routes - they should be handled by their specific endpoints
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Check if it's a static file in the dist root (like vite.svg, favicon.ico, etc.)
    static_file = static_dir / full_path
    if static_file.exists() and static_file.is_file():
        return FileResponse(static_file)
    
    # For all other routes, serve the SPA
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        raise HTTPException(status_code=404, detail="Frontend not built. Run 'cd web && npm run build' first.")

def main():
    import uvicorn
    print("🚀 Running at http://localhost:5000/")
    print("📚 API documentation available at http://localhost:5000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)

if __name__ == "__main__":
    main()
