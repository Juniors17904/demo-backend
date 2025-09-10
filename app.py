from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API de prueba funcionando 🚀"

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()

    # Si envían un número
    if "valor" in data:
        valor = data.get("valor", 0)
        resultado = valor * 2
        return jsonify({"resultado": resultado})

    # Si envían un texto
    if "texto" in data:
        texto = data.get("texto", "")
        resultado = "Procesado: " + texto.upper()
        return jsonify({"resultado": resultado})

    # Si no envían nada válido
    return jsonify({"error": "Debes enviar 'valor' (número) o 'texto' (string)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
