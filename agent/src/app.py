import logging
import os
from uuid import uuid4

import uvicorn
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.graph.graph import graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv() # pylint: disable=wrong-import-position

app = FastAPI(
    title="Blog Post Generator API",
    description="API for generating blog posts using LangGraph",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="blog-post-generator",
            description="Blog post generator agent that generates blog posts.",
            graph=graph,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway deployment."""
    try:
        # Basic application state check
        app_state = {
            "status": "healthy",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "timestamp": str(uuid4())
        }
        
        logger.info("Health check passed")
        return app_state
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Run the uvicorn server."""
    try:
        port = int(os.getenv("PORT", "8000"))
        logger.info(f"Starting server on port {port}")
        uvicorn.run(
            "src.app:app",
            host="0.0.0.0",
            port=port,
            reload=True,
            reload_dirs=["."],
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
