import os
import requests
#import workingpre
#import specNplot

from flask import Flask, render_template, request, redirect, jsonify, abort
from flask_dropzone import Dropzone
import moviepy.editor

app = Flask(__name__)
dropzone = Dropzone(app)
if __name__ == '__main__':
    app.debug = True
    app.run()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/player")
def player():
    return render_template("player.html")



app.config['MAX_CONTENT_LENGTH'] = 5000 * 5000 * 100000
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = ['.mov', '.mp4', '.m4v', '.3gp', '.mkv', '.mpeg', '.ogg',
                                   '.webm', '.wmv']
app.config['DROPZONE_PARALLEL_UPLOADS'] = 1

# If a file is too big, you'll get this. 
@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        if request.files:
            video = request.files.get('file')

            
        # Check if the file name was left blank or isn't in the extensions list. 
            if video.filename != '':
                file_ext = os.path.splitext(video.filename)[1]
            if file_ext not in app.config['DROPZONE_ALLOWED_FILE_TYPE']:
                return 'file not supported', 400
            video.save(os.path.join('static/uploads', video.filename))
            video_ta=moviepy.editor.VideoFileClip('static/uploads/'+ video.filename +"")
            audio=video_ta.audio
            audio.write_audiofile('static/uploads/audio/extracted_audio.wav')
            return redirect('player.html')
#            workingpre.call("static/uploads/audio")
#            specNplot.callspec()
    return render_template('player.html')


