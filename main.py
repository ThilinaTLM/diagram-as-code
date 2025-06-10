from diagrams import Diagram as _Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from flask import Flask, send_file, request, jsonify
import io
import os
import tempfile
import sys
from contextlib import redirect_stdout, redirect_stderr

app = Flask(__name__)

# Import available diagram components
AVAILABLE_COMPONENTS = {
    'aws': {
        'compute': {
            'EC2': EC2
        }
    },
    'onprem': {
        'client': {
            'Users': Users
        },
        'database': {
            'PostgreSQL': PostgreSQL
        },
        'network': {
            'Nginx': Nginx
        }
    }
}

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

def execute_diagram_code(code):
    """Execute Python code to generate a diagram and return as BytesIO object"""
    with tempfile.TemporaryDirectory() as temp_dir:
        diagram_path = os.path.join(temp_dir, "diagram")
        
        # Create a safe execution environment
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sorted': sorted,
                'sum': sum,
                'min': max,
                'max': max,
            },
            # Diagram-related imports - use our wrapper
            'Diagram': DiagramWrapper,
            'Cluster': Cluster,
            'EC2': EC2,
            'Users': Users,
            'PostgreSQL': PostgreSQL,
            'Nginx': Nginx,
            # File path for saving
            'diagram_path': diagram_path,
            'tempfile': tempfile,
            'os': os,
        }
        
        # Add more diagram components as needed
        try:
            # Import common diagram components dynamically
            from diagrams.aws import analytics, compute, database, network, storage
            from diagrams.onprem import client, database as onprem_db, network as onprem_net
            from diagrams.gcp import analytics as gcp_analytics, compute as gcp_compute
            
            safe_globals.update({
                'aws_analytics': analytics,
                'aws_compute': compute,
                'aws_database': database,
                'aws_network': network,
                'aws_storage': storage,
                'onprem_client': client,
                'onprem_database': onprem_db,
                'onprem_network': onprem_net,
                'gcp_analytics': gcp_analytics,
                'gcp_compute': gcp_compute,
            })
        except ImportError:
            pass  # Some modules might not be available
        
        safe_locals = {}
        
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
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

@app.route('/diagram', methods=['POST'])
def execute_diagram():
    """Execute Python code to generate a diagram"""
    try:
        # Get the code from request body
        if request.content_type == 'application/json':
            data = request.get_json()
            code = data.get('code')
        else:
            # Accept raw text as Python code
            code = request.get_data(as_text=True)
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Execute the code and generate diagram
        img_data, error = execute_diagram_code(code)
        
        if error:
            return jsonify({'error': error}), 400
        
        if img_data:
            return send_file(
                img_data,
                mimetype='image/png',
                as_attachment=False,
                download_name='executed_diagram.png'
            )
        else:
            return jsonify({'error': 'No diagram was generated'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Failed to execute code: {str(e)}'}), 500

def main():
    print("🚀 Running at http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()
