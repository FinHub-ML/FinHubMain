from flask import Flask, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import yt_dlp
from yt_dlp.postprocessor import FFmpegPostProcessor
import tempfile

from whisper_client.link_to_audio import download_audio
from whisper_client.whisper import transcribe

from urllib import parse
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
cors = CORS(app)  # Allow all origins for all routes
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
FFmpegPostProcessor._ffmpeg_location.set('./ffmpeg')



def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    try:
        print("VALUE parsing: ", value)
        url_parsed = parse.urlparse(value)
        qsl = parse.parse_qs(url_parsed.query)
        
        return qsl["v"][0]
    except:
        print("ERROR: ", value)
        return value
def download_and_transcribe_audio(url):
    error_code = download_audio(url)
    print("ERROR CODE: "    + str(error_code))
    
    id = video_id(url)
    
    filepath = f'./downloads/{id}.mp3'
    print("FILE PATH] " , filepath)

    text = transcribe(filepath)
    print("FINISHED TRANSCRIPTION")
    return text

@app.route('/transcribe_audio', methods=['GET'])
def transcribe_audio_route():
    url = request.args.get('url')
    if url:
        try:
            transcription = download_and_transcribe_audio(url)
            return transcription, 200
        except Exception as e:
            return f'Error occurred: {str(e)}', 500
    else:
        return 'No URL provided', 400

if __name__ == '__main__':
    app.run(debug=True)