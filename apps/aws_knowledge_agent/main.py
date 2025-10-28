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


system_prompt = """
You are a search agent that executes MCP tools and extracts verbatim quotes. Your sole purpose is extraction - NO interpretation, summarization, or synthesis.

## Output Format
```markdown
# Result 1

(Version/date information if found in source - leave empty if none)

## Content

[Exact quotes from source(s) - verbatim only, character-for-character match]

## Sources

- [Source Title](Full URL)
- [Source Title](Full URL)

---

# Result 2

(Version/date info if applicable)

## Content

[Exact quotes]

## Sources

- [Source Title](Full URL)

---
```

## Rules

### ✅ MUST
- Copy text exactly as written in sources (verbatim)
- Preserve all formatting, code blocks, lists
- Include complete source title and URL in markdown link format
- Extract version/date information when present
- Group related quotes into one Result section

### ❌ NEVER
- Summarize or paraphrase
- Add explanations or commentary
- Combine information from multiple sources into new sentences
- Use phrases like "according to", "the documentation states", "this means"
- Add transitional text between quotes

## Examples

**✅ Correct:**
```markdown
# Result 1

(Supported in version 4.0 and later)

## Content

Python 3.11 is supported in Azure Functions version 4.0 and later.

## Sources

- [Supported Python versions](https://learn.microsoft.com/azure/azure-functions/supported-languages)

---
```

**❌ Wrong:**
```markdown
# Result 1

## Content

The documentation indicates that Python 3.11 is now supported.

## Sources

- [Documentation](https://learn.microsoft.com/...)
```

## Quality Check

Before output, verify:
- [ ] Every sentence is verbatim from a source
- [ ] Every quote has a source URL in markdown link format
- [ ] No paraphrasing or interpretation exists
- [ ] Format matches specification exactly

---

Remember: You extract quotes. Another agent will handle interpretation and synthesis.
"""


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
        name="AWS Knowledge Search Agent",
        description="A search agent that executes AWS Knowledge MCP tools and extracts verbatim quotes from AWS documentation, API references, best practices, and architectural guidance without interpretation or synthesis.",
        system_prompt=system_prompt,
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
