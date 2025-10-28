from strands import Agent
from strands.models import BedrockModel
from strands_tools.a2a_client import A2AClientToolProvider

provider = A2AClientToolProvider(known_agent_urls=["http://127.0.0.1:10000"])

bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
)

agent = Agent(model=bedrock_model, tools=provider.tools)

response = agent(
    "pick an agent and make a sample call: Amazon S3 Vectors とは何ですか ?"
)

print(response)
