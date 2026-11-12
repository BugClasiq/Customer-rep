"""Entry point: the Gradio Support AI Assistant.

Launch with `python run.py`. The Flask API in app/ is independent and is not
started by this entrypoint.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.main import create_app


if __name__ == "__main__":
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    port = int(os.getenv("GRADIO_SERVER_PORT") or os.getenv("PORT") or "7860")
    print(f"Launching Support AI Assistant on http://{host}:{port} ...")
    create_app().launch(server_name=host, server_port=port, share=False)
