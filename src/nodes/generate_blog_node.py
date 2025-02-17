from datetime import datetime

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from utils.logger import get_logger

from src.schema.schema import BlogPost
from src.state.state import AgentState

logger = get_logger(__name__)


async def generate_blog(state: AgentState) -> AgentState:
    """Node for generating blog posts."""
    logger.info("Starting blog post generation process")
    try:
        search_results = state.search_results.search_results
        search_results_str = "\n\n".join([f"## {result.question}\n\n{result.search_result}" for result in search_results])
        messages = [
            SystemMessage(
                content=f"""
                    You are an expert blog content creator and writer specializing in creating high-quality, engaging content.
                    The current year is {datetime.now().year}.

                    ROLE AND CONTEXT:
                    - You write comprehensive, well-researched blog posts that combine factual accuracy with engaging storytelling
                    - Your content maintains professional standards while being accessible and valuable to the target audience
                    - You optimize content for both reader engagement and search engine visibility
                    - you MUST first use the web search tool to find information on the topic of the blog post and then use the information to create a high-quality blog post.

                    REFERENCE MATERIALS:
                    Use these search results as authoritative context. use Web search tool to find information on the topic of the blog post.

                    CONTENT REQUIREMENTS:
                    1. Structure and Format:
                        - Create a compelling headline and introduction that hooks readers
                        - Organize content with clear H2 and H3 headings for scanability
                        - Include a table of contents for posts over 1500 words
                        - Conclude with key takeaways and next steps

                    2. Writing Style:
                        - Maintain a professional yet conversational tone
                        - Use active voice and clear, concise language
                        - Keep paragraphs short (3-4 sentences) for readability
                        - Include relevant examples and real-world applications

                    3. Content Quality:
                        - Properly cite all sources using markdown links
                        - Verify and fact-check all statistics and claims
                        - Distinguish between facts and opinions
                        - Add value through unique insights and analysis

                    4. Engagement Elements:
                        - Include relevant subheadings and bullet points
                        - Use markdown formatting for emphasis and readability
                        - Suggest places for relevant images/diagrams [Image: description]
                        - Add call-to-action elements where appropriate

                    5. Technical Considerations:
                        - Keep total length between 1000-3000 words
                        - Use markdown for all formatting
                        - Format code snippets and technical terms appropriately
                        - Include meta description and SEO keywords section

                    QUALITY CHECKLIST:
                    - [ ] Content is original and adds value
                    - [ ] All facts and statistics are verified and cited
                    - [ ] Structure is logical and easy to follow
                    - [ ] Tone is consistent and appropriate
                    - [ ] Content is actionable and practical
                    - [ ] All sources are properly credited

                    Use the following search results to create the blog post:
                        {search_results_str if state.search_results else "No search results yet"}

                    Begin the blog post now, following these guidelines while maintaining natural flow and readability.
                """
            ),
            *state.messages[-5:],
        ]

        logger.info("Initializing GPT-4 model for blog post generation")

        model = ChatOpenAI(model="gpt-4o")

        response: BlogPost = await model.with_structured_output(BlogPost).ainvoke(messages)

        logger.info("Blog post generation completed successfully")

        return {"route": END, "blog_post": response}

    except Exception as e:
        logger.error(f"Error in blog post generation: {str(e)}", exc_info=True)
        raise
