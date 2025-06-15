from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import torch

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load summarization pipeline (this may take a few seconds initially)
device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"summary": "Please enter some text to summarize."})

        # Limit input length to avoid errors (BART limit is ~1024 tokens)
        if len(text.split()) > 500:
            return jsonify({"summary": "Please enter shorter text (below 500 words)."})

        # Generate summary
        summary_output = summarizer(text, max_length=120, min_length=30, do_sample=False)
        summary = summary_output[0]['summary_text']

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"summary": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
