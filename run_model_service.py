#!/usr/bin/env python3
"""Run local FastAPI model service."""
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "model_service.api:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
