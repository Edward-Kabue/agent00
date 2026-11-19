import os
import azure.cognitiveservices.speech as speechsdk
# call client for the project
speech_config = speechsdk.SpeechConfig(
    subscription=os.environ["SPEECH_KEY"],
    endpoint=os.environ["SPEECH_ENDPOINT"],
)
speech_config.speech_recognition_language = "en-US"
# call the speech recognizer for the project
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config
)


# output the recognized text to the console
print("Speak into your microphone.")
result = recognizer.recognize_once_async().get()


if (
    result is not None
    and result.reason == speechsdk.ResultReason.RecognizedSpeech
):
    print("RECOGNIZED:", result.text)
elif (result is not None and result.reason == speechsdk.ResultReason.NoMatch):
    print("No speech could be recognized.")
elif (result is not None and result.reason == speechsdk.ResultReason.Canceled):
    print("Canceled:", result.cancellation_details.reason)
