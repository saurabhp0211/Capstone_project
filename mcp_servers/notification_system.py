from mcp.server.fastmcp import FastMCP
import uuid
from datetime import datetime

mcp = FastMCP("NotificationSystem")

@mcp.tool()
def log_and_notify(action_taken: str, summary: str) -> dict:
    """Logs the final case and sends a mock notification."""
    
    case_id = f"CASE-{uuid.uuid4().hex[:6].upper()}"
    
    return {
        "action_taken": action_taken,
        "notification_sent": True,
        "case_id": case_id,
        "timestamp": datetime.now().isoformat(),
        "summary": summary
    }