from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS 
import requests
import os

app = Flask(__name__)
CORS(app)

api_key = "6555c3e2e244bd3e3c849b3434312e92"

@app.route('/Style.css')
def serve_css():
    return send_from_directory('.', 'Style.css')

@app.route('/about.css')
def serve_about_css():
    return send_from_directory('.', 'about.css')

# Serve images from Img folder
@app.route('/Img/<path:filename>')
def serve_images(filename):
    return send_from_directory('Img', filename)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/About.html')
def about():
    return send_file('About.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city or len(city) > 50:
        return jsonify({"error": "City name required (max 50 characters)"}), 400
    
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        data = response.json()
        url = "http://127.0.0.1:1234/v1/chat/completions"
        model_name = "llama-3.2-3b-instruct"
        payload = {
                    "model": model_name,
                    "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Short Weather update in Chennai"}
                        ]
                }
        chatresponse = requests.post(url, json=payload)
        if response.status_code == 200 or chatresponse.status_code == 200:
            if chatresponse.status_code == 200:
                reply = chatresponse.json()["choices"][0]["message"]["content"]
                weather_info=f"Assistant: {reply}"
                return jsonify({
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "condition": data["weather"][0]["description"].title(),
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "Weather_i":weather_info
                })
        elif response.status_code == 404:
            return jsonify({"error": "City not found. Please try again."}), 404
        else:
            return jsonify({"error": "Something went wrong with the weather API"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to weather service"}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)