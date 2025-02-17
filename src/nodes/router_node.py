from typing import Any

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END

from src.schema.nodes import CHAT, GENERATE_BLOG, WEB_SEARCH
from src.schema.schema import AssessIntent
from src.state.state import AgentState
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def router_assessment(state: AgentState) -> AssessIntent:
    """Assess the user's intent and determine the next action."""
    logger.info("Starting router assessment")
    try:
        system_message = SystemMessage(
            content=f"""
            You are a blog post writing assistant that helps users create high-quality blog posts.
            Your goal is to determine the appropriate next action based on the user's request.

            Current blog post state:
            {state.blog_post if state.blog_post else "No blog post generated yet"}

            Current search results state:
            {state.search_results if state.search_results else "No search results yet"}

            Analyze the conversation and determine:
            1. If we need to search for information (only if no search results exist)
            2. If we need to generate/modify a blog post (only if search results exist)
            3. If we should just chat with the user

            Provide your assessment following the AssessIntent schema.
            """
        )

        model = ChatOpenAI(model="gpt-4o")

        assessment = await model.with_structured_output(AssessIntent).ainvoke([system_message, *state.messages[-5:]])

        logger.info(f"Router assessment complete: {assessment.dict()}")
        return assessment

    except Exception as e:
        logger.error(f"Error in router assessment: {str(e)}", exc_info=True)
        raise


def goto_route(state: AgentState) -> Any:
    """Determine if we should end or continue routing."""
    if state.route == END or state.route == "__end__":
        logger.info("Routing to END state")
        return END
    return state.route


async def router(state: AgentState) -> AgentState:
    """Main router function that determines the next action."""
    logger.info("Starting main router function")
    try:
        assessment = await router_assessment(state)

        if assessment.generate_blog_post.boolean_value:
            logger.info("Routing to blog post generation")
            return {"route": GENERATE_BLOG}
        elif assessment.search_web.boolean_value:
            logger.info("Routing to web search")
            return {"route": WEB_SEARCH}
        else:
            logger.info("Routing to chat")
            return {"route": CHAT}

    except Exception as e:
        logger.error(f"Error in main router: {str(e)}", exc_info=True)
        raise
