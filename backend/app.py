from flask import Flask, request, send_file, jsonify
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

from bart.bart import financial_summarizer, financial_summarizer_sample_usage

from top_news import get_processed_news_list, bert_get_sentiment

load_dotenv()

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "https://finhub-ml.github.io"}})
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


# ----------------- BART -----------------
@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.json.get('text')  # Expect JSON data in the request body
    if text:
        try:
            key_points, entities = financial_summarizer_sample_usage(text)
            response = {
                'key_points': key_points,
                'entities': entities
            }
            print(response)
            return jsonify(response), 200
        except Exception as e:
            return str(e), 500
    else:
        return 'No text provided', 400




# ----------------- BERT -----------------
# TODO: Implement BERT API



@app.route('/news', methods=['GET'])
def get_news():
    news_list = get_processed_news_list()
    return jsonify(news_list)

@app.route('/get_sentiment', methods=['POST'])
def get_sentiment():
    text = request.json.get('text')
    if text:
        try:
            sentiment = bert_get_sentiment(text)
            return jsonify(sentiment), 200
        except Exception as e:
            return str(e), 500
    else:
        return 'No text provided', 400


# ----------------- Stable Diffusion -----------------
# TODO: Implement Stable Diffusion API
@app.route('/latest_image', methods=['GET'])
def get_latest_image():
    try:
        # Get the list of generated images from the 'images' folder
        image_files = os.listdir('images')
        
        if image_files:
            # Sort the image files based on their modification time (latest first)
            image_files.sort(key=lambda x: os.path.getmtime(os.path.join('images', x)), reverse=True)
            
            # Get the filename of the latest generated image
            latest_image = image_files[0]
            
            # Construct the path to the latest image file
            image_path = os.path.join('images', latest_image)
            
            return send_file(image_path, mimetype=f'image/{latest_image.split(".")[-1]}')
        else:
            return 'No generated images found', 404
    except Exception as e:
        return str(e), 500
    
    
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