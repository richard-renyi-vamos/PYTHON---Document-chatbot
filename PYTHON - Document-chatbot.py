import os
from transformers import pipeline
from flask import Flask, request, jsonify

# Load the document
def load_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        document = file.read()
    return document

document_text = load_document('document.txt')

# Initialize the NLP model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")

# Create Flask app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('question')
    if user_input:
        response = qa_pipeline(question=user_input, context=document_text)
        answer = response['answer']
        return jsonify({'answer': answer})
    return jsonify({'answer': 'Please ask a question about the document.'})

if __name__ == '__main__':
    app.run(debug=True)
