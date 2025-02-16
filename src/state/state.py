from datetime import datetime
from typing import Annotated, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph.message import Messages
from langgraph.graph.message import add_messages as og_add_messages
from pydantic import BaseModel, Field
from schema.schema import BlogPost, SearchResults


def add_messages(left: Messages, right: Messages) -> Messages:
    """Wraps langchain's add_messages to add custom logic"""
    for message in right:
        message.additional_kwargs["created_at"] = datetime.now().isoformat()
    return og_add_messages(left, right)


class AgentState(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages] = Field(default=[])
    blog_post: BlogPost = Field(default_factory=BlogPost)
    route: Optional[str] = Field(default=None)
    search_results: SearchResults = Field(default_factory=SearchResults)
