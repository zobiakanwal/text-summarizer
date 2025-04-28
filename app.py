from flask import Flask, render_template, request
import requests
from gtts import gTTS
import os

# Initialize Flask app
app = Flask(__name__)

# Hugging Face API details
API_KEY = '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'  # Replace with your Hugging Face API key
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def summarize_text(text):
    try:
        # Send the text to Hugging Face API for summarization
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        if response.status_code == 200:
            # Successfully received a response
            return response.json()[0]['summary_text']
        else:
            # Log the error details from Hugging Face API for debugging
            print(f"Error: {response.status_code}")
            print(response.json())  # Output the error message from Hugging Face
            return "Error in summarization. Please try again later."
    except Exception as e:
        # Log any exception that occurs
        print(f"Exception: {e}")
        return "Error in summarization. Please try again later."

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    input_text = ''
    if request.method == 'POST':
        input_text = request.form.get('text', '')
        if input_text:
            # Summarize the input text using Hugging Face API
            summary = summarize_text(input_text)
            
            # Generate audio file from summary using gTTS
            tts = gTTS(text=summary, lang='en')
            audio_path = os.path.join('static', 'summary.mp3')
            tts.save(audio_path)
    
    return render_template('index.html', summary=summary, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
