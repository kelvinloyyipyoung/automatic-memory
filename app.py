import os
from flask import Flask, render_template, request, redirect, url_for
from google import genai

app = Flask(__name__)

# FIXME remove key before launch
api_key = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key="AIzaSyB02DwcZbwiRqxbhVbzdOVwz5Y1ANgmel0")

@app.route('/')
def dashboard():
    response_text = request.args.get('response_text', '')
    return render_template('dashboard.html', response_text=response_text)

@app.route('/submit', methods=['POST'])
def submit():
    video_game = request.form['video-game']
    query = f"""Where can I play {video_game}? 
    Format the answer as a json object, 
    with each console as a key and the value as the store where the game is available."""
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=query
    )
    response_text = response.text
    response_text = response_text.lstrip("```json").rstrip("`").strip()
    return redirect(url_for('dashboard', response_text=response_text))

if __name__ == '__main__':
    app.run(debug=True)
