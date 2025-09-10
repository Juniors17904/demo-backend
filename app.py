from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API de prueba funcionando 🚀"

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()
    texto = data.get("texto", "")
    resultado = "Procesado: " + texto.upper()
    return jsonify({"resultado": resultado})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
