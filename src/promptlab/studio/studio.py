import asyncio
import logging
import signal
import sys
from pathlib import Path

from art import tprint
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from promptlab.studio.studio_api import StudioApi
from promptlab.tracer.tracer import Tracer


class Studio:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer
        self.shutdown_event = asyncio.Event()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def print_welcome_text(port: int) -> None:
        """Print the welcome text and port number.

        Args:
            port (int): The port number to display
        """

        tprint("PromptLab")
        print(f"\n🚀 PromptLab Studio läuft unter: http://localhost:{port} 🚀")

    def create_web_app(self):
        """Create a production-ready FastAPI app that serves both API and static files"""
        studio_api = StudioApi(self.tracer)
        app = studio_api.get_app()

        # Mount static files using FastAPI's StaticFiles
        static_path = Path(__file__).resolve().parent.parent / "web"
        if static_path.exists():
            app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

        # Serve index.html for SPA routes
        @app.get("/")
        @app.get("/datasets")
        @app.get("/prompts")
        async def serve_spa():
            return FileResponse(str(static_path / "index.html"))

        # Health check endpoint
        @app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "promptlab-studio"}

        return app

    def setup_signal_handlers(self):
        """Setup graceful shutdown signal handlers"""

        def signal_handler(signum, frame):
            self.logger.info(
                f"Signal {signum} empfangen, starte geordnetes Herunterfahren..."
            )
            self.shutdown_event.set()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def start_async(self, port: int = 8000, workers: int = 1):
        """
        Async start method using FastAPI for both API and static files.
        """
        try:
            self.print_welcome_text(port)
            app = self.create_web_app()
            self.setup_signal_handlers()

            config = uvicorn.Config(
                app,
                host="0.0.0.0",
                port=port,
                workers=workers,
                log_level="info",
                access_log=True,
                # Production optimizations (use uvloop on Unix systems)
                loop="uvloop" if sys.platform != "win32" else "asyncio",
                http="httptools" if sys.platform != "win32" else "h11",
                # Security headers
                server_header=False,
                date_header=False,
                # Connection settings
                timeout_keep_alive=5,
            )

            server = uvicorn.Server(config)
            server_task = asyncio.create_task(server.serve())

            self.logger.info(f"PromptLab Studio gestartet unter http://localhost:{port}")

            # Wait for shutdown signal
            await self.shutdown_event.wait()

            # Graceful shutdown
            self.logger.info("Starte geordnetes Herunterfahren...")
            server.should_exit = True
            await server_task

        except Exception as e:
            self.logger.error(f"Fehler beim Starten von PromptLab Studio: {e}")
            raise e
