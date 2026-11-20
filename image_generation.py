import os
import base64
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True)

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client()

result = openai.images.generate(
    model=os.environ["IMAGE_MODEL_DEPLOYMENT_NAME"],
    prompt=(
        "A cast iron bicycle rack shaped like a wave, on a rainy "
        "city street at dusk, photographed on 35mm film, wide shot"
    ),
    n=1,
    size="1024x1024",
    quality="high",
    output_format="png",
)
if not result.data or not result.data[0].b64_json:
    raise RuntimeError("No image data returned")
image_bytes = base64.b64decode(result.data[0].b64_json)
with open("generated_image.png", "wb") as f:
    f.write(image_bytes)
print("Image generated and saved as 'generated_image.png'")
