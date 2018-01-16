from app import app
import os
from flask import render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from .twitch_chat_word_counter import ChatLog
import pandas as pd

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'irc'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('count',
                                    filename=filename))

    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/count')
def count():
    filename = request.args.get('filename')
    chat = ChatLog(app.config['UPLOAD_FOLDER']+ '/' + filename)
    counter = chat.gen_counter()
    pd.set_option('display.max_colwidth', -1)
    df = pd.DataFrame(counter.most_common(15))
    df.columns = ['Spam', 'Count']

    return render_template('count.html', table=df.to_html(classes='table', index=False, border=0))


@app.route('/get-transcripts')
def get_transcripts():
    return render_template('get-transcripts.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS