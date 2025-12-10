"""FastAPI main application entry point."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from typing import Optional

from .config import settings
from .database import init_db, get_db
from .dependencies import get_current_user
from .models import User
from .utils.security import decode_access_token
from .websocket.manager import ConnectionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "development" else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Discord Clone API",
    description="A full-featured Discord clone backend with real-time messaging",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use settings.allowed_origins_list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Discord Clone Backend...")
    init_db()
    logger.info("Database initialized")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Server running on {settings.HOST}:{settings.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Discord Clone Backend...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Discord Clone API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.websocket("/ws/{user_id}/{server_id}/{channel_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    server_id: int,
    channel_id: int,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time messaging.
    
    Args:
        websocket: WebSocket connection
        user_id: User ID
        server_id: Server ID
        channel_id: Channel ID
        token: JWT authentication token
        db: Database session
    """
    # Verify token
    if not token:
        await websocket.close(code=1008, reason="Authentication required")
        return
    
    payload = decode_access_token(token)
    if not payload or payload.get("sub") != user_id:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    # Accept connection
    await manager.connect(websocket, user_id, server_id, channel_id)
    
    try:
        # Notify others that user joined
        await manager.broadcast(
            {
                "type": "user_join",
                "data": {
                    "user_id": user_id,
                    "channel_id": channel_id
                }
            },
            channel_id,
            exclude_user=user_id
        )
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            
            # Broadcast message to all users in channel
            await manager.broadcast(
                {
                    "type": "message",
                    "data": data
                },
                channel_id
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id, server_id, channel_id)
        
        # Notify others that user left
        await manager.broadcast(
            {
                "type": "user_leave",
                "data": {
                    "user_id": user_id,
                    "channel_id": channel_id
                }
            },
            channel_id
        )
        
        logger.info(f"User {user_id} disconnected from channel {channel_id}")


# Import and include routers
from .routes import auth, users, servers, channels, messages

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(servers.router, prefix="/servers", tags=["Servers"])
app.include_router(channels.router, prefix="/channels", tags=["Channels"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
