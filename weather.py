from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests
app=Flask(__name__)
CORS(app)
api_key="6555c3e2e244bd3e3c849b3434312e92"
@app.route('/get_weather', methods=['GET'])
def get_weather():
    city=request.args.get('city')
    if not city or len(city)>50:
        return jsonify({"City Name required"}),400
    try:
        response=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        data=response.json()
        if (response.status_code==200):
            return jsonify({
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "condition": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"]
               })
        elif(response.status_code==404):
            return jsonify({"City not found. Please try again."}),404
        else:
            return jsonify({"error": "Something went wrong with the API"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)