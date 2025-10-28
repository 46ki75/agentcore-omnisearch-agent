import uuid
import asyncio
import httpx

from a2a.client import ClientFactory, ClientConfig
from a2a.types import Message, Part, Role, TextPart, TaskArtifactUpdateEvent
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("omnisearch_mcp")


AGENT_URL = "http://127.0.0.1:10000/"


async def run():

    httpx_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=10.0,
            read=300.0,
            write=30.0,
            pool=10.0,
        )
    )

    config = ClientConfig(httpx_client=httpx_client)

    client = await ClientFactory.connect(AGENT_URL, client_config=config)

    message = Message(
        messageId=str(uuid.uuid4()),
        role=Role.user,
        parts=[Part(root=TextPart(text="Amazon S3 Vectors とは何ですか？"))],
    )

    artifacts = []
    async for response in client.send_message(message):
        if isinstance(response, tuple):
            task, update_event = response
            if isinstance(update_event, TaskArtifactUpdateEvent):
                artifacts.append(update_event.artifact)
            elif task.artifacts:
                artifacts = task.artifacts

    text = ""

    for artifact in artifacts:
        for part in artifact.parts:
            if isinstance(part.root, TextPart):
                text = text + part.root.text

    return text


if __name__ == "__main__":
    result = asyncio.run(run())
    print(result)
