# Graph as Code Online

A web application that generates diagrams from Python code using the `diagrams` library, built with FastAPI backend and Svelte frontend.

## Features

- 🎨 Interactive web interface for writing diagram code
- 🐍 Python-based diagram generation using the `diagrams` library
- 🚀 FastAPI backend with automatic API documentation
- ⚡ Vite + Svelte frontend with modern UI
- 🐳 Docker containerization with multi-stage builds
- 🔄 Health checks and monitoring
- 🌐 SPA routing support

## Quick Start

### Using Docker (Recommended)

1. **Build and run everything:**
   ```bash
   ./scripts/build-and-run.sh
   ```

2. **Or manually with Docker Compose:**
   ```bash
   # Build frontend first
   cd web && pnpm install && pnpm run build && cd ..
   
   # Build and run containers
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:5000
   - API docs: http://localhost:5000/docs
   - Health check: http://localhost:5000/health

### Development Setup

1. **Backend (Python):**
   ```bash
   # Install dependencies
   uv sync
   
   # Run development server
   uv run python main.py
   ```

2. **Frontend (Svelte):**
   ```bash
   cd web
   pnpm install
   pnpm run dev  # Development server on http://localhost:5173
   pnpm run build  # Production build
   ```

## Docker Configuration

### Basic Usage
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down
```

### With Nginx Proxy
```bash
# Run with nginx reverse proxy on port 8080
docker-compose --profile with-proxy up -d
```

### Production Deployment
```bash
# Remove development volume mounts in docker-compose.yml
# Then build and deploy
docker-compose -f docker-compose.yml up --build -d
```

## API Endpoints

- `POST /diagram` - Generate diagram from Python code
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation
- `GET /*` - Serve frontend SPA (catch-all)

## Example Diagram Code

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Web Service", show=False):
    ELB("lb") >> EC2("web") >> RDS("userdb")
```

## Project Structure

```
.
├── main.py                 # FastAPI backend
├── pyproject.toml         # Python dependencies
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Container orchestration
├── nginx.conf            # Nginx reverse proxy config
├── scripts/
│   └── build-and-run.sh  # Build helper script
└── web/                  # Frontend Svelte app
    ├── src/
    ├── dist/             # Built frontend (served by FastAPI)
    ├── package.json
    └── vite.config.ts
```

## Environment Variables

- `PYTHONUNBUFFERED=1` - Ensure Python output is not buffered

## Health Monitoring

The application includes health checks:
- Docker health check every 30s
- HTTP endpoint at `/health`
- Nginx proxy health monitoring

## Troubleshooting

1. **Frontend not loading:**
   - Ensure `web/dist` exists: `cd web && pnpm run build`
   - Check Docker build logs: `docker-compose logs`

2. **Diagram generation fails:**
   - Verify graphviz is installed in container
   - Check Python code syntax
   - Review API error messages at `/docs`

3. **Port conflicts:**
   - Change ports in `docker-compose.yml`
   - Default: 5000 (app), 8080 (nginx)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test locally
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
