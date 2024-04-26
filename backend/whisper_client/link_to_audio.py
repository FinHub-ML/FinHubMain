import yt_dlp

from yt_dlp.postprocessor import FFmpegPostProcessor
FFmpegPostProcessor._ffmpeg_location.set('./ffmpeg')

# URL = "https://www.youtube.com/watch?v=MhT5bdSTAbw"
def download_audio(URL):
    ydl_opts = {
        'outtmpl': '/downloads/%(id)s',
        'format': 'mp3/bestaudio/best',
        'keepvideo': False,
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',

        }]
    } 

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
        error_code = ydl.download(URL)
    return error_code

# download_audio("https://www.youtube.com/watch?v=H_gHb1S5qc4")
