from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END

from src.schema.schema import BlogPost
from src.state.state import AgentState
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def feedback_node(state: AgentState) -> AgentState:
    """Node for updating the blog post based on feedback."""
    logger.info("Starting blog post generation process")
    try:
        messages = [
            SystemMessage(
                content=f"""
                You are a helpful assistant that updates the blog post based on the feedback.

                The blog post is:
                <BlogPost>
                {state.blog_post}
                </BlogPost>

                Pay attention to the user messages below for the feedback and update the blog post accordingly.
                Make sure to keep the original content of the blog post, just update the parts that are mentioned in the feedback.
                """
            ),
            *state.messages[-5:],
        ]

        model = ChatOpenAI(model="gpt-4o")

        response: BlogPost = await model.with_structured_output(BlogPost).ainvoke(messages)

        logger.info("Blog post updated successfully")

        return {"route": END, "blog_post": response}

    except Exception as e:
        logger.error(f"Error in blog post generation: {str(e)}", exc_info=True)
        raise
