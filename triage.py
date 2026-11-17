import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# this calls authetication and gets the openai client for the project
openai = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
).get_openai_client()

# this calls the text analytics client for the project
# note this calls the tools from the azure.ai.textanalytics package,
# not the openai client
endpoint = os.environ["LANGUAGE_ENDPOINT"]
key = os.environ["LANGUAGE_KEY"]
client = TextAnalyticsClient(endpoint=endpoint,
                             credential=AzureKeyCredential(key))

reviews = [
    "The delivery was late and the box was crushed. Very disappointing.",
    "Fantastic service from Contoso. Ravi sorted the whole thing in minutes.",
    "The app works. Nothing special, nothing wrong.",
]


# function to triage a review, returning sentiment, key phrases
# named entities, and a summary
def triage(review):
    sentiment = client.analyze_sentiment([review])[0]
    phrases = client.extract_key_phrases([review])[0].key_phrases[:3]
    found = client.recognize_entities([review])[0].entities
    names = [e.text for e in found if e.category in ("Person", "Organization")]
    summary = openai.responses.create(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="Summarise this review in one sentence, under 15 words.",
        input=review,
    ).output_text
    return sentiment.sentiment, phrases, names, summary


print(f"{'MOOD':<10}{'KEY PHRASES':<36}{'WHO':<22}SUMMARY")
for review in reviews:
    mood, phrases, names, summary = triage(review)
    print(
        f"{mood:<10}{', '.join(phrases) or '-':<36}"
        f"{', '.join(names) or '-':<22}{summary}"
    )
