from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API de prueba funcionando 🚀"

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()

    # Si recibe un texto
    if "texto" in data:
        texto = data.get("texto", "")
        return jsonify({"resultado": f"Procesado: {texto.upper()}"})

    # Si recibe un número
    if "valor" in data:
        valor = data.get("valor", 0)
        try:
            valor = float(valor)
            return jsonify({"resultado": valor * 2})
        except ValueError:
            return jsonify({"error": "El valor debe ser numérico"}), 400

    return jsonify({"error": "Debes enviar 'texto' o 'valor'"}), 400
