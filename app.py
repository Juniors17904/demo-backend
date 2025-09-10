from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API de prueba funcionando 🚀"

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debes enviar un dato"}), 400

    # Si mandas con clave "texto"
    if "texto" in data:
        valor = str(data.get("texto", "")).strip()

        if valor.isdigit():
            return jsonify({"resultado": f"'{valor}' es un número"})
        elif valor.isalpha():
            return jsonify({"resultado": f"'{valor}' es una letra"})
        else:
            return jsonify({"resultado": f"'{valor}' es mixto (letras y números)"})

    return jsonify({"error": "Debes enviar 'texto'"}), 400
