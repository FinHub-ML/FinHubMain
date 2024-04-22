from openai import OpenAI
import os 
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Create a client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)


# File path 
## Transcribe from English
def transcribe(file):
    audio_file= open(file, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)


## Translation
def translate():
    audio_file= open("/path/to/file/german.mp3", "rb")
    translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file
    )
    print(translation.text)
    
file_path = "./sample_audio/sample1.mp3"
transcribe(file_path)