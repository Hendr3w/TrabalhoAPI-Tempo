from flask import Flask, jsonify
import requests
import redis
import json

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

API_TEMPO_URL = "http://localhost:5001/weather/"

@app.route("/recommendation/<city>", methods=["GET"])
def get_recommendation(city):
    city_key = city.replace(" ", "").capitalize()

    cached_data = r.get(city_key)

    if cached_data:
        weather = json.loads(cached_data)
    else:
        try:
            response = requests.get(API_TEMPO_URL + city)
            if response.status_code != 200:
                return jsonify({"error": "Cidade nao encontrada"}), 404
            weather = response.json()
            r.setex(city_key, 60, json.dumps(weather))

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



    


        