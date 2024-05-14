# FinHub

## Backend 
### 1. Create Venv, install requirements, and activate
.venv\Scripts\activate
cd backend
pip install -r requirements.txt
.venv\Scripts\activate
### 2. Create .env file, set environment key 
OPENAI_API_KEY = paste-my-key-here

STABILITY_KEY = paste-my-key-here

NEWS_API_KEY = paste-my-key-here


### 3. ffmpeg install (for link-to-audio)
#### Windows
- download from https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
- move the ffmpeg.exe and ffprobe.exe to backend/whisper_client/ffmpeg/
#### Mac (Please contact if problem, not tested since no MAC machine)
- brew install ffmpeg
### 4. Download our finetuned BERT model
- https://drive.google.com/drive/folders/1f73MSmtG9qHJW4UkEI_FxGBl9dYQqUye?usp=drive_link

# Docs
- Planning page: https://docs.google.com/document/d/1Z7vSNdYFWoE4q9VNosy1tkRNSG_z8pdKKVhqWxOz6K0/edit
- Sample output page: https://docs.google.com/document/d/1gipkOAjggENA84eLiepr1C2xSv_gs1408usCCPYQ7HA/edit?usp=sharing

