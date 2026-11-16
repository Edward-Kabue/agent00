import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


SYSTEM_PROMPT = """You are a support triage assistant for Pedalworks.
Classify the customer message into exactly one of: delivery,
faulty-product, refund, other. Reply with the label only, lower case.
If it fits none of them, reply: other."""

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client()
agent = project.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="You are a study assistant for the AI-901 exam. "
                     "Keep answers under 120 words. If a question is "
                     "not about AI-901 or Azure, say so.",
    ),
)
print(f"Agent: {agent.name}, version: {agent.version}, id: {agent.id}")
