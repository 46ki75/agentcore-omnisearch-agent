import logging
import os
import time
from strands import Agent
from strands.multiagent.a2a import A2AServer
import uvicorn
from fastapi import FastAPI
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient


logging.basicConfig(level=logging.INFO)

# Use the complete runtime URL from environment variable, fallback to local
runtime_url = os.environ.get("AGENTCORE_RUNTIME_URL", "http://127.0.0.1:9000/")

logging.info(f"Runtime URL: {runtime_url}")


streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client("https://knowledge-mcp.global.api.aws")
)

with streamable_http_mcp_client:

    tools = streamable_http_mcp_client.list_tools_sync()

    strands_agent = Agent(
        name="Calculator Agent",
        description="A calculator agent that can perform basic arithmetic operations.",
        tools=[tools],
        callback_handler=None,
    )

    host, port = "0.0.0.0", 9000

    # Pass runtime_url to http_url parameter AND use serve_at_root=True
    a2a_server = A2AServer(
        agent=strands_agent,
        http_url=runtime_url,
        serve_at_root=True,  # Serves locally at root (/) regardless of remote URL path complexity
    )

    app = FastAPI()

    @app.get("/ping")
    def ping():
        return {"status": "Healthy", "time_of_last_update": int(time.time())}

    app.mount("/", a2a_server.to_fastapi_app())

    if __name__ == "__main__":
        uvicorn.run(app, host=host, port=port)
