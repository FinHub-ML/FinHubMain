from openai import OpenAI
import os 
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Create a client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

## Transcribe from English
def transcribe():
    audio_file= open("./sample_audio/sample1.mp3", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)

# Summary
# Google (company) in the US (location) is undergoing a major reorganization to accelerate AI product development (positive). 
# CEO Sundar Pichai is shifting the company culture towards more business-focused norms, moving away from its historically open, 
# socially-involved workplace (negative). This change is emphasized by the recent dismissal of nearly 30 employees protesting a significant Israeli government contract, 
# highlighting a new, stricter stance on employee activism (negative).


## Translation
def translate():
    audio_file= open("/path/to/file/german.mp3", "rb")
    translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file
    )
    print(translation.text)
    

# transcribe()