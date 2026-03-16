from flask import Flask, request, render_template
from transformers import pipeline
from datetime import datetime
app = Flask(__name__)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text'].strip().replace('\n', ' ')    
    if not text:
        return render_template('index.html', original="", summary="Please enter valid text.")
    max_len = min(512, int(len(text.split()) * 1.5))
    min_len = max(30, int(len(text.split()) * 0.3))
    result = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
    with open("summaries.txt", "a", encoding='utf-8') as f:
        f.write(f"\n--- {datetime.now()} ---\nOriginal:\n{text}\n\nSummary:\n{result}\n\n")
    return render_template('index.html', original=text, summary=result)
if __name__ == '__main__':
    app.run(debug=True)
