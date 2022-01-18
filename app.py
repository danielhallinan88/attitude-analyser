from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api, reqparse
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
api = Api(app)

def polarity_emotion_analysis(text):
    polarity_scores = sia.polarity_scores(text)
    emotion_scores = text2emotion.get_emotion(text)
    summary = {}
    summary['polarity_scores'] = polarity_scores
    summary['emotion_scores'] = emotion_scores
    return summary

def get_hits(sentences, get_dependencies):
    hits = []

    for sentence in sentences:
        doc = nlp(sentence)
        hit = {}
        hit['text'] = sentence
        hit['polarity_emotion_scores'] = polarity_emotion_analysis(sentence)

        # https://spacy.io/usage/linguistic-features
        if get_dependencies:
            token_dep_dict = { int(idx) : { 'token' : token.text, 'dep' : token.dep_, 'start_idx' : token.idx } for idx, token in enumerate(doc)}
            hit['tokens_pos'] = token_dep_dict

        hits.append(hit)

    return hits

def process_text(text, summary_only, get_dependencies):
    doc = nlp(text)

    tokens = [ token.text for token in doc ]
    sentences = [str(i) for i in doc.sents]

    template = dict()
    template['hit_count'] = len(sentences)

    if summary_only:
        pass
    else:
        template['hits'] = get_hits(sentences, get_dependencies)

    template['summary'] = polarity_emotion_analysis(text)
    return template

# curl -d '{"key1":"value1"}'  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-text
# curl -d '{"text":"I like coffee. He likes tea."}'  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-text  | jq
# curl -d @data.json  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-text  | jq

class Test(Resource):
    def get(self):
        return {'test': 'success'}

class AnalyzeText(Resource):
    def post(self):
        start = time.time()
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, required=True)
        parser.add_argument('summary_only', type=bool)
        parser.add_argument('get_dependencies', type=bool)
        args = parser.parse_args()

        text = args['text']
        summary_only = args['summary_only'] if args['summary_only'] else False
        get_dependencies = args['get_dependencies'] if args['get_dependencies'] else False

        return_vals = process_text(text, 
            summary_only, 
            get_dependencies
            )

        return_vals['process_time'] = time.time() - start
        return jsonify(return_vals)

api.add_resource(Test, '/test')
api.add_resource(AnalyzeText, '/api/v1.0/analyze-text')

if __name__ == '__main__':
    app.run(debug=True)
