import asyncio
from typing import Optional
from uuid import uuid4

from graph.graph import get_blog_post_generator_graph
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from schema.schema import BlogPost, SearchResults
from state.state import AgentState

# Constants
MODEL_NAME = "gpt-4o"
DEFAULT_PROMPT = "Generate a blog post about the latest trends in AI"

class BlogPostValidator(BaseModel):
    """Validator model for blog post verification."""
    is_valid: bool = Field(description="Whether the blog post aligns with the user's request.")
    feedback: str = Field(description="Feedback on the blog post, if it is not valid.")

class BlogPostGenerator:
    """Handles blog post generation and validation."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    async def generate(self) -> dict:
        """Generate a blog post using the graph."""
        try:
            graph = get_blog_post_generator_graph()
            default_state = self._create_default_state()
            thread_id = str(uuid4())

            result = await graph.ainvoke(
                input=default_state,
                config={"configurable": {"thread_id": thread_id}}
            )

            print(result['messages'][-1])
            return result

        except Exception as e:
            print(f"Error generating blog post: {e}")
            raise

    async def validate(self, result: dict) -> bool:
        """Validate the generated blog post."""
        try:
            if not self._validate_result_structure(result):
                return False

            messages = self._create_validation_prompt(result)
            validation_response = self.llm.with_structured_output(BlogPostValidator).invoke(messages)

            if not validation_response.is_valid:
                print(f"Blog post validation failed. Feedback: {validation_response.feedback}")
                return False

            print("Blog post is valid and aligns with the user's request.")
            return True

        except Exception as e:
            print(f"Error during blog post validation: {e}")
            return False

    @staticmethod
    def _create_default_state() -> AgentState:
        """Create default state for blog post generation."""
        return AgentState(
            messages=[HumanMessage(content=DEFAULT_PROMPT)],
            blog_post={"title": "", "content": ""},
            search_results={"search_results": []}
        )

    @staticmethod
    def _validate_result_structure(result: Optional[dict]) -> bool:
        """Validate the structure of the generation result."""
        try:
            assert result is not None, "Result is None, expected a valid result object."
            assert 'messages' in result, "Result does not contain 'messages'."
            assert 'blog_post' in result, "Result does not contain 'blog_post'."
            assert 'search_results' in result, "Result does not contain 'search_results'."
            return True
        except AssertionError as e:
            print(f"Validation error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during structure validation: {e}")
            return False

    @staticmethod
    def _create_validation_prompt(result: dict) -> list:
        """Create the validation prompt from the result."""
        return [
            HumanMessage(content=f"""
                Validate the following blog post content to ensure it aligns with the user's request:
                <User's Request>
                    {result['messages'][0].content}
                </User's Request>
                <Blog Post Content>
                    {result['blog_post'].content}
                </Blog Post Content>
                """.strip())
        ]

async def main():
    """Main execution function."""
    try:
        generator = BlogPostGenerator()
        result = await generator.generate()
        await generator.validate(result)
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())

