from app import app
from flask import render_template, url_for


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/count/<filename>')
def count():
    return render_template('count.html')


@app.route('/get-transcripts')
def get_transcripts():
    return render_template('get-transcripts.html')
