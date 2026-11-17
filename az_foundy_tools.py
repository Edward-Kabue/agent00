import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

endpoint = os.environ["LANGUAGE_ENDPOINT"]
key = os.environ["LANGUAGE_KEY"]
client = TextAnalyticsClient(endpoint=endpoint,
                             credential=AzureKeyCredential(key))

reviews = [
    "The delivery was late and the box was crushed. Very disappointing.",
    "Fantastic service from Contoso. Ravi sorted the whole thing in minutes.",
    "The app works. Nothing special, nothing wrong.",
]


phrase_results = client.extract_key_phrases(reviews)
for result in phrase_results:
    print(result.key_phrases)

entity_results = client.recognize_entities(reviews)
for result in entity_results:
    for entity in result.entities:
        print(entity.text, "|", entity.category,
              "|", round(entity.confidence_score, 2),
              "| offset", entity.offset)
