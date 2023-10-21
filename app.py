import os
from flask import Flask, request, send_file
from moviepy.editor import AudioFileClip, VideoFileClip
from werkzeug.utils import secure_filename
import threading
import time

app = Flask(__name__)
def delete_mp3_files(folder):
    time.sleep(60)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if file_path.endswith(".mp3"):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error while deleting file {file_path}: {e}")

@app.route('/convert', methods=['POST'])
def convert_to_mp3():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    file_path = os.path.join('./uploads', filename)  # Save the file in the 'uploads' folder
    file.save(file_path)

    try:
        video = VideoFileClip(file_path)
        audio = video.audio
    except Exception as e:
        try:
            audio = AudioFileClip(file_path)
        except Exception as e:
            return f"Error during file upload: {e}"

    try:
        audio_file_path = os.path.join('./uploads', 'output.mp3')
        audio.write_audiofile(audio_file_path)
        response = send_file(audio_file_path, as_attachment=True)
        os.remove(file_path)  # Remove the original file after download
        threading.Thread(target=lambda: delete_mp3_files(rf".\uploads")).start()
        return response
    except Exception as e:
        return f"An error occurred during the conversion: {e}"

if __name__ == '__main__':
    app.run(debug=True)
