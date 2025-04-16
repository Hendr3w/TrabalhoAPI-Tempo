from flask import Flask, jsonify

app = Flask(__name__)

weather_data = {
    "SaoPaulo": {"temp": 25, "unit": "Celsius"},
    "RioDeJaneiro": {"temp": 32, "unit": "Celsius"},
    "Curitiba": {"temp": 12, "unit": "Celsius"}
}

@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    city_key = city.replace(" ", "").capitalize()
    if city_key in weather_data:
        return jsonify({"city": city, **weather_data[city_key]})
    else:
        return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == "__main__":
    app.run(port=5001, debug=True)