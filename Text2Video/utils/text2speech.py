import requests
from io import BytesIO
import base64
from pydub import AudioSegment
import os
def TextToSpeech(text, gender, source_language):
    audio_payload = {
        "controlConfig": {"dataTracking": True},
        "input": [{"source": text}],
        "config": {"gender": gender, "language": {"sourceLanguage": source_language}},
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Content-Type": "application/json",
    }
    audio_data = requests.post(
        url=os.environ['TEXT_TO_SPEECH_ENDPOINT'],  
        json=audio_payload,
        headers=headers,
    )
    audio_data.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    audio_resp_data = audio_data.json()
    save_directory='audio'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    audio_data = base64.b64decode(audio_resp_data["audio"][0]["audioContent"])
    audio_stream = BytesIO(audio_data)

    output_file=os.path.join(os.getcwd(), 'audio/audio.wav')
    with open(output_file, "wb") as output_file:
        output_file.write(audio_data)

    return audio_stream,output_file



