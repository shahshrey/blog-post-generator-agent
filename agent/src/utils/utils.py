import json
from typing import Any


def format_log_content(content: Any) -> str:
    """Format content for logging with proper indentation and line breaks."""
    if isinstance(content, (dict, list)):
        return f"\n{json.dumps(content, indent=2)}"
    elif isinstance(content, str):
        if "```" in content or "{" in content:
            return f"\n{content}"
        return content
    return str(content)
