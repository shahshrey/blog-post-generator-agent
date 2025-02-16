import logging

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from nodes.chat_node import chat_with_user
from nodes.generate_blog_node import generate_blog
from nodes.router_node import goto_route, router
from nodes.web_search_node import search_web
from schema.nodes import CHAT, GENERATE_BLOG, ROUTER, WEB_SEARCH
from state.state import AgentState

_ = load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Disable noisy HTTP request logs
for log_name in ["httpx", "httpcore"]:
    log = logging.getLogger(log_name)
    log.setLevel(logging.WARNING)


def build_graph() -> CompiledGraph:
    """Build and compile the state graph."""
    logger.info("Building state graph")

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node(ROUTER, router)
    graph.add_node(GENERATE_BLOG, generate_blog)
    graph.add_node(CHAT, chat_with_user)
    graph.add_node(WEB_SEARCH, search_web)

    # Set entry point
    graph.set_entry_point(ROUTER)

    # Add conditional edges
    graph.add_conditional_edges(
        ROUTER,
        goto_route,
        {
            GENERATE_BLOG: GENERATE_BLOG,
            WEB_SEARCH: WEB_SEARCH,
            CHAT: CHAT,
            END: END,
        },
    )

    graph.add_edge(WEB_SEARCH, GENERATE_BLOG)
    graph.add_edge(GENERATE_BLOG, END)
    graph.add_edge(CHAT, END)

    logger.info("State graph built successfully")
    return graph.compile()


_graph = None


def get_blog_post_generator_graph() -> CompiledGraph:
    """Get the compiled graph, creating it if necessary."""
    global _graph
    _graph = build_graph()
    return _graph
