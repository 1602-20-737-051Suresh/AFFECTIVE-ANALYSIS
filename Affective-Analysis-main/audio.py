from app import app

from flask import render_template,Response,url_for

# import pandas as pd

from SpeechEmotionRecognition import speechEmotionRecognition
import os
import csv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            with open(event.src_path, 'r') as f:
                reader = csv.reader(f)
                data = list(reader)
            return render_template('AudioAnalysis.html', data=data)

@app.route('/main/audio')
def audio():
    speechEmotionRecognition(os.path.join('Models', 'audio.hdf5'))
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return render_template('AudioAnalysis.html', data=data, url_for=url_for)


event_handler = CSVHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()