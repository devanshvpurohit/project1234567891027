from flask import Flask, request, render_template
import sign_language_translator as slt
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load GitHub raw README snippet (still sucks intentionally)
    code_snippet = requests.get("https://raw.githubusercontent.com/sign-language-translator/sign-language-translator/main/README.md").text[:300]
    
    # Check if video exists
    video_url = "/static/out.mp4" if os.path.exists("static/out.mp4") else None
    return render_template('index.html', code_snippet=code_snippet, video_url=video_url)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    model = slt.models.ConcatenativeSynthesis(
        text_language="english",
        sign_language="pk-sl",
        sign_format="video"
    )
    sign = model.translate(text)

    # Save video
    out_path = "static/out.mp4"
    sign.save(out_path, overwrite=True)
    return render_template('index.html', video_url=f"/{out_path}", code_snippet="")
