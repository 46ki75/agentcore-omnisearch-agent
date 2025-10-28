import asyncio
from strands import Agent
from strands import Agent
from strands.models import BedrockModel
from strands_tools.a2a_client import A2AClientToolProvider

system_prompt = """
pick an agent and make a sample call
"""

agent_provider = A2AClientToolProvider(known_agent_urls=["http://127.0.0.1:10000"])

bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
)

strands_agent = Agent(
    name="Enduser Agent",
    description="A helpful assistant.",
    system_prompt=system_prompt,
    tools=agent_provider.tools,
    callback_handler=None,
    model=bedrock_model,
)


# Async function that iterates over streamed agent events
async def process_streaming_response():
    prompt = "What is Amazon S3 Vectors ?"

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
