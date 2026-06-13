from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, health, uploads, documents, outlines, notes, exports, presentations, content
from app.services.persistence import store


def create_app() -> FastAPI:
    app = FastAPI(
        title="SlideGen AI API",
        description="SlideGen AI — presentations, content studio, and prompt-to-design API.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(uploads.router, prefix="/api/v1", tags=["uploads"])
    app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
    app.include_router(outlines.router, prefix="/api/v1", tags=["outlines"])
    app.include_router(notes.router, prefix="/api/v1", tags=["notes"])
    app.include_router(exports.router, prefix="/api/v1", tags=["exports"])
    app.include_router(presentations.router, prefix="/api/v1", tags=["presentations"])
    app.include_router(content.router, prefix="/api/v1", tags=["content"])

    @app.on_event("shutdown")
    def close_persistence_connections() -> None:
        store.close()

    return app


app = create_app()
