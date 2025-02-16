import os
from datetime import datetime
from typing import List

import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from schema.nodes import GENERATE_BLOG
from schema.schema import SearchResult, SearchResults
from state.state import AgentState
from utils.logger import get_logger

logger = get_logger(__name__)


class SearchInput(BaseModel):
    questions: List[str] = Field(
        description=""" The list of questions to search for based on the topic for blog posts. Create a list of questions based on topic to create the blog post.

        Example:
        user: I want to write a blog post about the latest trends in AI.
        Example questions:
        "What are the latest trends in AI?"
        "What are the latest trends in generative AI?"
        "What are the latest trends in LLMs?"
        "What are the latest trends in RAG?"
        "What are the latest trends in agentic AI?"
        """
    )


async def generate_questions(state: AgentState) -> List[str]:
    logger.info("Generating search questions from user input")
    try:
        SYSTEM_PROMPT = f"""
        You are an expert web researcher. Your task is to formulate relevant questions
        for searching information about the blog topic requested by the user.

        The current year is {datetime.now().year}.
        The current date is {datetime.now().strftime("%Y-%m-%d")}.
        Create a list of 5-8 specific questions that will help gather comprehensive
        information for the blog post.

        Review the last messages and create a list of questions that will help gather comprehensive
        information for the blog post.
        """
        messages = [SystemMessage(SYSTEM_PROMPT), *state.messages[-5:]]

        model = ChatOpenAI(model="gpt-4o").with_structured_output(SearchInput)

        response: SearchInput = await model.ainvoke(messages)
        logger.info(f"Generated {len(response.questions)} questions for web search")
        return response.questions
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}", exc_info=True)
        raise


async def search_web(state: AgentState) -> AgentState:
    logger.info("Starting web search process")
    try:
        headers = {"X-API-Key": str(os.getenv("YDC_API_KEY"))}
        results = []
        messages = state.messages[-5:]

        model = ChatOpenAI(model="gpt-4o")
        questions = await generate_questions(state)

        for i, question in enumerate(questions, 1):
            logger.info(f"Processing search question {i}/{len(questions)}: {question}")
            try:
                search_results = requests.get(
                    "https://api.ydc-index.io/search",
                    params={"query": question},
                    headers=headers,
                )
                search_results.raise_for_status()

                messages = [
                    SystemMessage(
                        """
                        You are a blog writer. Your task is to write a blog post based on the topic provided by the user.
                        Ensure you provide an answer that is a direct and clear response to the question.
                        """
                    ),
                    HumanMessage(
                        content=f"""
                        Use the following search results to help answer the question:

                        SEARCH QUERY formed from the user question:
                        -------------
                        {question}
                        -------------
                        SEARCH RESULTS:
                        ---------------
                        {search_results.json()}
                        ---------------
                        Instructions:
                        1. Provide a direct and clear answer to the question.
                        2. Focus only on information relevant to the question asked.
                        3. Do not include any additional information not directly related to the question.
                        4. Make sure you only provide the answer to the question asked and nothing else.
                        5. Provide a detailed and accurate response based on the information available in a professional manner in markdown format.
                        6. Cite all the sources of your information in the response based on the search results. This is very important. DO NOT make up sources or miss any.
                        7. Your response should just be a summary of search results as an answer with sources.
                        8. when mentioning sources, use markdown links with the name of the source as the text and the url as the link to make them clickable. example: [AI trends](https://www.google.com/ai-trends)
                        """
                    ),
                ]

                response = await model.ainvoke(messages)

                results.append(SearchResult(question=question, search_result=response.content))
                logger.info(f"Successfully processed search results for question {i}")

            except requests.RequestException as e:
                logger.error(
                    f"Error in web search for question {question}: {str(e)}",
                    exc_info=True,
                )
                continue
            except Exception as e:
                logger.error(
                    f"Error processing search results for question {question}: {str(e)}",
                    exc_info=True,
                )
                continue

        logger.info(f"Completed web search process with {len(results)} results")
        search_results = SearchResults(search_results=results)
        return {"route": GENERATE_BLOG, "search_results": search_results}

    except Exception as e:
        logger.error(f"Fatal error in search_web: {str(e)}", exc_info=True)
        raise
