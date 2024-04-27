from flask import Flask, request, send_file
from openai import OpenAI
import os
from dotenv import load_dotenv
from yt_dlp.postprocessor import FFmpegPostProcessor
import tempfile

from urllib import parse
from flask_cors import CORS

from whisper_client.link_to_audio import download_audio
from whisper_client.whisper import transcribe

from sd_client.sd import generate_SD3
load_dotenv()

app = Flask(__name__)
cors = CORS(app)  # Allow all origins for all routes
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
FFmpegPostProcessor._ffmpeg_location.set('./ffmpeg')

# ----------------- Whisper API / Link to Audio -----------------
# Input: URL of video 
# Process: Downloads audio from video -> Transcribes audio
# Output: Transcription of audio in video
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

# ----------------- BERT -----------------
# TODO: Implement BERT API






# ----------------- Stable Diffusion -----------------
# TODO: Implement Stable Diffusion API

@app.route('/generate_image', methods=['POST'])
def generate_head_image():
    prompt = request.form.get('prompt')
    negative_prompt = request.form.get('negative_prompt', '')
    aspect_ratio = request.form.get('aspect_ratio', '16:9')
    seed = int(request.form.get('seed', 0))
    output_format = request.form.get('output_format', 'png')
    model = request.form.get('model', 'sd3')

    if prompt:
        try:
            generated_image_path = generate_SD3(
                prompt,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio,
                seed=seed,
                output_format=output_format,
                model=model
            )
            return send_file(generated_image_path, mimetype=f'image/{output_format}')
        except Exception as e:
            return str(e), 500
    else:
        return 'No prompt provided', 400
if __name__ == '__main__':
    app.run(debug=True)