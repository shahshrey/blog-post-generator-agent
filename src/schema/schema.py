from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ReasonedBoolean(BaseModel):
    reason: str = Field(description="The reason for the boolean value")
    boolean_value: bool = Field(description="The boolean value")

class GenerateBlogPost(ReasonedBoolean):
    pass

class ChatWithUser(ReasonedBoolean):
    pass

class SearchWeb(ReasonedBoolean):
    pass

class AssessIntent(BaseModel):
    generate_blog_post: GenerateBlogPost = Field(description="""
        Whether to generate the blog post based on the user's request.
        Set to True if:
        - They are asking to generate a blog post
        - They are providing feedback on the existing blog post
        - They want to modify or improve an existing blog post
        """)
    search_web: SearchWeb = Field(description="""
        Whether to search the web for information.
        Set to True if:
        - We need to gather information for a new blog post
        - We need to update information in an existing blog post
        - We need to fact-check or verify information
        """)
    chat_with_user: ChatWithUser = Field(description="""
        Whether to chat with the user.
        Set to True if:
        - They are asking general questions
        - They need clarification
        - They are not specifically requesting blog post generation
        """)
    
class BlogPost(BaseModel):
    title: str
    content: str
    search_results: Optional[List[Dict[str, str]]] = Field(default_factory=list)    