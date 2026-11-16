import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    CodeInterpreterTool,
    PromptAgentDefinition,
)

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
agent = project.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="You help with AI-901 study questions. Use the "
                     "code interpreter when a question needs arithmetic.",
        tools=[CodeInterpreterTool()]
    ),
)
print(f"Agent: {agent.name}, version: {agent.version}")

openai = project.get_openai_client()
response = openai.responses.create(
    input=(
        "If 1,000 tokens is 750 words, how many tokens is a 12,000"
        " word document?"
    ),
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"}
    },
)
print(response.output_text)
project.agents.delete_version(
    agent_name=os.environ["AGENT_NAME"],
    agent_version=agent.version,
)
print("Agent version deleted.")
