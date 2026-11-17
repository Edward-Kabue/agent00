import json
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()
SYSTEM = (
    "You analyse customer reviews. Reply with JSON only, no prose. "
    'Use exactly these keys: "sentiment" (one of positive, negative, '
    'neutral), "key_phrases" (up to three strings), "entities" '
    '(strings), "summary" (one sentence under 15 words).'
)
reviews = [
    "The delivery was late and the box was crushed. Very disappointing.",
    "Fantastic service from Contoso. Ravi sorted the whole thing in minutes.",
    "The app works. Nothing special, nothing wrong.",
]
answer = openai.responses.create(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions=SYSTEM,
    input=reviews[0]
)
print(json.loads(answer.output_text))
