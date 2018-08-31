from app import app
import os
from flask import render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from twitchchatspamcounter.tcsc import ChatLog
import pandas as pd
from .helper import txt_to_emote


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'irc', 'log'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '23908479qroaqweilf34'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected')
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
    chat = ChatLog(app.config['UPLOAD_FOLDER'] + '/' + filename)
    counter = chat.gen_counter()
    pd.set_option('display.max_colwidth', -1)
    df = pd.DataFrame(counter.most_common(100))
    df.columns = ['Spam', 'Count']
    df = txt_to_emote(df)
    pog, lul, r = chat.poglul_ratio()
    poglul_str = f'{r:{4}.{3}} ({pog} PogChamp: {lul} LUL)'
    os.remove(app.config['UPLOAD_FOLDER'] + '/' + filename)

    return render_template('count.html', table=df.to_html(classes='table', index=False, border=0, justify='left', escape=False), poglul_str=poglul_str)


@app.route('/get-transcripts')
def get_transcripts():
    return render_template('get-transcripts.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS