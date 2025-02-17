from uuid import uuid4

from langchain_core.messages import HumanMessage

from graph.graph import get_blog_post_generator_graph
from schema.schema import BlogPost, SearchResults
from state.state import AgentState

async def main():
    graph = get_blog_post_generator_graph()

    default = AgentState(
        messages = [
            HumanMessage(content="Generate a blog post about the latest trends in AI")
        ],
        blog_post = {
            "title": "",
            "content": "",
        },
        search_results={
            "search_results": []
        }
    )
    result = None
    thread_id = uuid4()

    while True:
        result = await graph.ainvoke(
            input=result if result else default,
            config={
                "configurable": {
                    "thread_id": str(thread_id)
                }
            }
        )
        print(result['messages'][-1])
        next = input("message: ")
        result['messages'].append(HumanMessage(content=next))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 