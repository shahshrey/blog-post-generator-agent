import logging
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from src.graph.graph import get_blog_post_generator_graph
from src.state.state import AgentState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Blog Post Generator API",
    description="API for generating blog posts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    blog_post: dict
    messages: list

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Blog Post Generator API")
    try:
        # Verify environment and dependencies
        logger.info("Verifying environment and dependencies...")
        # Add any initialization code here if needed
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.post("/generate", response_model=GenerateResponse)
async def generate_blog_post(request: GenerateRequest):
    try:
        logger.info("Received generate request")
        graph = get_blog_post_generator_graph()

        initial_state = AgentState(
            messages=[
                HumanMessage(content=request.prompt)
            ],
            blog_post={
                "title": "",
                "content": "",
            },
            search_results={
                "search_results": []
            }
        )

        thread_id = uuid4()
        logger.info(f"Processing request with thread_id: {thread_id}")

        result = await graph.ainvoke(
            input=initial_state,
            config={
                "configurable": {
                    "thread_id": str(thread_id)
                }
            }
        )

        logger.info("Successfully generated blog post")
        return GenerateResponse(
            blog_post=result['blog_post'],
            messages=[msg.content for msg in result['messages']]
        )
    except Exception as e:
        logger.error(f"Error generating blog post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        # Add more comprehensive health checks
        logger.info("Health check requested")

        # Check if environment variables are set
        required_env_vars = ["PORT"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            raise HTTPException(status_code=500, detail=f"Missing environment variables: {missing_vars}")

        # Add basic application state check
        app_state = {
            "status": "healthy",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "port": os.getenv("PORT", "8000"),
            "timestamp": str(uuid4())
        }

        logger.info(f"Health check passed: {app_state}")
        return app_state
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 8000))
        logger.info(f"Starting server on port {port}")
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
