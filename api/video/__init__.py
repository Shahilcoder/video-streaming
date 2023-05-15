import os
import time
import requests
import ffmpeg
from flask import Blueprint, Response

video = Blueprint('video', __name__, url_prefix='/video')


@video.route("/", methods=("GET",))
def video_index():
    return "Video api"


@video.route("/sample", methods=("GET",))
def get_sample():
    def generate():
        """Generator function"""
        url = "https://getsamplefiles.com/download/mkv/sample-1.mkv"
        input_path = "./api/video/input.mkv"
        output_path = "./api/video/output.mp4"

        print("Downloading...")
        response = requests.get(url, stream=True)

        # download the video file in chunks
        with open(input_path, "wb") as input_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    input_file.write(chunk)
            
            input_file.close()
            

        if os.path.exists(output_path):
            os.remove(output_path)
        
        # convert the video into mp4 format (universally supported)
        print("Converting...")
        ffmpeg.input(input_path).output(output_path, codec='copy').run()

        if os.path.exists(input_path):
            os.remove(input_path)
        
        # stream the video in chunks
        video_path = output_path
        with open(video_path, 'rb') as video_file:
            while True:
                video_chunk = video_file.read(1024)
                if not video_chunk:
                    break
                yield video_chunk

    # returning generator object as response
    return Response(generate(), mimetype='video/mp4')
