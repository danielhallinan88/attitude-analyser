from flask import Flask, request, jsonify, abort
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import nltk
import spacy
import text2emotion
import time

# Init
nltk.data.path.append("nltk_data/")
sia = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

def polarity_emotion_analysis(text):
    polarity_scores = sia.polarity_scores(text)
    emotion_scores = text2emotion.get_emotion(text)
    summary = {}
    summary['polarity_scores'] = polarity_scores
    summary['emotion_scores'] = emotion_scores
    return summary

def get_hits(sentences):
    hits = []

    for sentence in sentences:
        hit = {}
        hit['text'] = sentence
        hit['polarity_emotion_scores'] = polarity_emotion_analysis(sentence)
        hits.append(hit)

    return hits

def process_text(text):
    doc = nlp(text)

    tokens = [ token.text for token in doc ]
    sentences = [str(i) for i in doc.sents]

    template = dict()
    template['hit_count'] = len(sentences)
    template['hits'] = get_hits(sentences)
    template['summary'] = polarity_emotion_analysis(text)
    return template

@app.route('/')
def test():
    return 'SUCCESS'

# curl -d '{"key1":"value1"}'  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-string
# curl -d '{"text":"I like coffee. He likes tea."}'  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-string  | jq
# curl -d @data.json  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-string  | jq
@app.route('/api/v1.0/analyze-string', methods=['POST'])
def analyze_string():
    start = time.time()
    data = json.loads(request.data)
    text = str(data['text'])

    return_vals = process_text(text)
    process_time = time.time() - start
    return_vals['process_time'] = process_time
    return jsonify(return_vals)

app.run()
