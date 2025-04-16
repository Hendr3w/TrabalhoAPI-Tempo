from flask import Flask, jsonify
import requests

app = Flask(__name__)

cache = {}

API_TEMPO_URL = "http://localhost:5001/weather/"

@app.route("/recommendation/<city>", methods=["GET"])
def get_recommendation(city):
    city_key = city.replace(" ", "").capitalize()

    if city_key in cache:
        weather = cache[city_key]
    else:
        try:
            response = requests.get(API_TEMPO_URL + city)
            if response.status_code != 200:
                return jsonify({"error": "Cidade nao encontrada"}), 404
            weather = response.json()
            cache[city_key] = weather
        except Exception as e:
            return jsonify({"error": "Erro ao Consultar API-Tempo"}), 500


    temp = weather["temp"]
    recommendation = ""

    if temp > 30:
        recommendation = "Esta quente! Beba agua e use protetor solar."
    elif 15 < temp <= 30:
        recommendation = "O clima esta agradavel. Aproveite o dia!"
    else:
        recommendation = "Esta frio! Não esqueça o casaco."


    return jsonify({
        "city": weather["city"],
        "temperature": f"{temp} ºC",
        "recommendation": recommendation
    })

if __name__=="__main__":
    app.run(port=5002, debug=True)



    


        