import os
import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
        
    # Create a bar chart
    labels = ['positive', 'negative', 'neutral']
    scores = [max(0, polarity), max(0, -polarity), 1 - abs(polarity)]
    
    fig, ax = plt.subplots()
    ax.bar(labels, scores)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({'sentiment': sentiment, 'plot_url': plot_url})

if __name__ == '__main__':
    app.run(port=8080, debug=True)
