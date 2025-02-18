import logging

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.nodes.chat_node import chat_with_user
from src.nodes.feedback_node import feedback_node
from src.nodes.generate_blog_node import generate_blog
from src.nodes.router_node import goto_route, router
from src.nodes.web_search_node import search_web
from src.schema.nodes import CHAT, FEEDBACK, GENERATE_BLOG, ROUTER, WEB_SEARCH
from src.state.state import AgentState

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



graph = StateGraph(AgentState)

# Add nodes
graph.add_node(ROUTER, router)
graph.add_node(GENERATE_BLOG, generate_blog)
graph.add_node(CHAT, chat_with_user)
graph.add_node(WEB_SEARCH, search_web)
graph.add_node(FEEDBACK, feedback_node)
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
        FEEDBACK: FEEDBACK,
        END: END,
    },
)

graph.add_edge(WEB_SEARCH, GENERATE_BLOG)
graph.add_edge(GENERATE_BLOG, END)
graph.add_edge(CHAT, END)
graph.add_edge(FEEDBACK, END)
memory = MemorySaver()
logger.info("State graph built successfully")
graph = graph.compile(checkpointer=memory)

def get_blog_post_generator_graph():
    """
    Returns the compiled blog post generator graph.
    """
    return graph

