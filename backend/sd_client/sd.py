import requests
import os 
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


STABILITY_KEY = os.environ.get("STABILITY_KEY")
def generate_image(prompt, aspect_ratio = "16:9", style_preset = "photographic"):
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer sk-MYAPIKEY",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "webp",
            "aspect_ratio": aspect_ratio,
            "style_preset": style_preset,
        },
    )

    if response.status_code == 200:
        with open("./dog-wearing-glasses.webp", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    
    

def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

# prompt = "This dreamlike digital art captures a vibrant, kaleidoscopic bird in a lush rainforest" #@param {type:"string"}
# negative_prompt = "" #@param {type:"string"}
# aspect_ratio = "1:1" #@param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
# seed = 0 #@param {type:"integer"}
# output_format = "jpeg" #@param ["jpeg", "png"]
# model = "sd3" #@param ["sd3", "sd3-turbo"]
def generate_SD3(prompt, negative_prompt="", aspect_ratio="16:9", seed=0, output_format="png", model="sd3"):


    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt if model=="sd3" else "",
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format" : output_format,
        "model" : model,
        "mode" : "text-to-image"
    }

    response = send_generation_request(
        host,
        params
    )

    # Decode response
    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")

    # Check for NSFW classification
    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")

    # Save and display result
    # generated = f"generated_{seed}.{output_format}"
    generated = os.path.join('images', f"generated_{seed}.{output_format}")
    with open(generated, "wb") as f:
        f.write(output_image)
    return generated

# generate_SD3()