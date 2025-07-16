from flask import Flask, request, render_template
import sign_language_translator as slt
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # pull GitHub file (just to show it sucks)
    code_snippet = requests.get("https://raw.githubusercontent.com/sign-language-translator/sign-language-translator/main/README.md").text[:300]
    return render_template('index.html', code_snippet=code_snippet)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    model = slt.models.ConcatenativeSynthesis(
        text_language="english",
        sign_language="pk-sl",
        sign_format="video"
    )
    sign = model.translate(text)
    sign.save("static/out.mp4", overwrite=True)
    return render_template('index.html', video_url="/static/out.mp4")

if __name__ == '__main__':
    app.run(debug=True)
