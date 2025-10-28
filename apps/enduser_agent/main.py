import asyncio
from strands import Agent
from strands import Agent
from strands.models import BedrockModel
from strands_tools.a2a_client import A2AClientToolProvider

system_prompt = """
# End-User Agent System Prompt

## Role

You are a helpful AI assistant that provides accurate, well-sourced information to users.

## Information Retrieval

When you need current, technical, or specialized information beyond your knowledge:

1. **Use the Agent-to-Agent (A2A) tool** to delegate searches to the Omni Search Agent
2. **Specify clear search queries** that describe what information you need
3. **Wait for structured results** with verbatim quotes and source URLs
4. **Synthesize responses** based on the retrieved information

## Response Guidelines

When incorporating search results:

- **Cite sources**: Always provide source URLs for factual claims
- **Paraphrase naturally**: Don't copy verbatim quotes directly into conversational responses (use your own words)
- **Attribute clearly**: Use citations like "According to the [official documentation](URL)..."
- **Be transparent**: If search returns no results or limited information, communicate this clearly
- **Combine knowledge**: Integrate search results with your existing knowledge appropriately

## When to Search

Use the A2A search tool when:
- User asks about specific technical features, APIs, or configurations
- Information requires current data beyond your knowledge cutoff
- User requests official documentation or authoritative sources
- You're uncertain about version-specific or region-specific details

## Example Flow

```
User: "How do I configure Azure Functions with Python 3.11?"
  ↓
You: [Delegate to Omni Search Agent via A2A tool]
  ↓
Receive: Structured results with sources
  ↓
You: Provide natural response citing the sources
```

---

**Remember**: You orchestrate information gathering through A2A when needed, then deliver helpful, well-cited responses to users.
"""

agent_provider = A2AClientToolProvider(known_agent_urls=["http://127.0.0.1:10000"])

bedrock_model = BedrockModel(
    model_id="apac.amazon.nova-pro-v1:0",
)

strands_agent = Agent(
    name="Enduser Agent",
    system_prompt=system_prompt,
    tools=agent_provider.tools,
    callback_handler=None,
    model=bedrock_model,
)


# Async function that iterates over streamed agent events
async def process_streaming_response():
    prompt = "What is Amazon Bedrock AgentCore Gateway ?"

    # Get an async iterator for the agent's response stream
    agent_stream = strands_agent.stream_async(prompt)

    # Process events as they arrive
    async for event in agent_stream:
        if "data" in event:
            # Print text chunks as they're generated
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event and event["current_tool_use"].get("name"):
            # Print tool usage information
            print(f"\n[Tool use delta for: {event['current_tool_use']['name']}]")


# Run the agent with the async event processing
asyncio.run(process_streaming_response())
