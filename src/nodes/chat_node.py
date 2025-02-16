import logging

from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from state.state import AgentState

logger = logging.getLogger(__name__)


async def chat_with_user(state: AgentState) -> AgentState:
    """Node for general chat interactions."""
    logger.info("Starting chat with user")
    system_message = SystemMessage(
        content="""
        You are a helpful assistant that can discuss blog writing
        and help users with their blog-related questions.
        """
    )

    model = ChatOpenAI(model="gpt-4o")
    response = await model.ainvoke([system_message, *state.messages[-5:]])

    return {"messages": [AIMessage(content=response.content)]}
