from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.api_core.client_options import ClientOptions

app = FastAPI()

# allow cross-origin (for local dev — React runs on port 3000, backend maybe 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
PROJECT_ID = "big-axiom-457001-f3"
STT_LOCATION = "us"  # or whatever region
client = SpeechClient(client_options=ClientOptions(
    api_endpoint=f"{STT_LOCATION}-speech.googleapis.com"
))

recognizer = client.recognizer_path(PROJECT_ID, STT_LOCATION, "_")
model = "chirp_3"

@app.get("/api/hello")
async def hello():
    config = cloud_speech.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    model=model,
    language_codes=["en-US"],
    )

    with open("sample.mp3", "rb") as f:
        audio_content = f.read()

    request = cloud_speech.RecognizeRequest(
        recognizer=recognizer,
        config=config,
        content=audio_content,
    )

    transcript_response = client.recognize(request=request)
    transcripts = [
        {"transcript": alt.transcript}
        for result in transcript_response.results
        for alt in result.alternatives
    ]
    return {"message": transcript_response.results}


@app.get("/api/hello2")
async def hello2():
    client = genai.Client(api_key="")
    upload_file = client.files.upload(file="sample.mp3")
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=["Transcribe the audio file subject", upload_file]
    )

    return {"message": response.text}



@app.get("/api/hello1")
async def hello1():
    client = genai.Client(api_key="")

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents="Explain how AI works in a few words",
    )

    return {"message": response.text}
