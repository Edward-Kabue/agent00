import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv(override=True)

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ["SPEECH_KEY"],
    endpoint=os.environ["SPEECH_ENDPOINT"])
speech_config.speech_synthesis_voice_name = "en-US-AvaNeural"

audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

result = synthesizer.speak_text_async("Your table is booked for Friday.").get()
assert result is not None
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Spoken successfully.")
elif result.reason == speechsdk.ResultReason.Canceled:
    details = result.cancellation_details
    print("Canceled:", details.reason, details.error_details)
