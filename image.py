import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True)

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client()

IMAGE_URL = (
    "https://fastly.picsum.photos/id/888/200/300.jpg?"
    "hmac=WJcjbSQSOOzfBpPsUKZHZzjBCJjDv43RwJ8P8Ag2xj4"
)

response = openai.responses.create(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    input=[{"role": "user", "content": [
        {"type": "input_text", "text": "What is in this image?"},
        {"type": "input_image", "image_url": IMAGE_URL,
         "detail": "auto"},
    ]}],
)
print(response.output_text)
