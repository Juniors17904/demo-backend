from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

def calcular_angulo(x1, y1, x2, y2):
    return np.arctan2(y2 - y1, x2 - x1)

def encontrar_linea_cercana(img, x1, y1, x2, y2, radio=40, dist_max=60):
    min_x = max(min(x1, x2) - radio, 0)
    max_x = min(max(x1, x2) + radio, img.shape[1])
    min_y = max(min(y1, y2) - radio, 0)
    max_y = min(max(y1, y2) + radio, img.shape[0])
    roi = img[min_y:max_y, min_x:max_x]
    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gris, 100, 220, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=10)
    mejor_linea = None
    mejor_score = 1e9
    angulo_marcado = calcular_angulo(x1, y1, x2, y2)
    if lines is not None:
        for l in lines:
            lx1, ly1, lx2, ly2 = l[0]
            lx1 += min_x
            lx2 += min_x
            ly1 += min_y
            ly2 += min_y
            angulo_detectado = calcular_angulo(lx1, ly1, lx2, ly2)
            dist = np.hypot(lx1-x1, ly1-y1) + np.hypot(lx2-x2, ly2-y2)
            angulo_diff = abs(angulo_marcado - angulo_detectado)
            score = dist + 300 * angulo_diff
            if score < mejor_score and dist < dist_max:
                mejor_score = score
                mejor_linea = (lx1, ly1, lx2, ly2)
    return mejor_linea

@app.route("/")
def home():
    return "API de procesamiento de tubos funcionando 🚀"

@app.route("/procesar", methods=["POST"])
def procesar():
    if "imagen" not in request.files or "lineas" not in request.form:
        return jsonify({"error": "Debes enviar una imagen y las líneas"}), 400

    archivo = request.files["imagen"]
    npimg = np.frombuffer(archivo.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Recibe las líneas marcadas por el usuario (JSON string)
    try:
        lineas_usuario = eval(request.form["lineas"])
    except Exception:
        return jsonify({"error": "Formato de líneas incorrecto"}), 400

    lineas_ajustadas = []
    for linea in lineas_usuario:
        x1, y1, x2, y2 = linea
        linea_ajustada = encontrar_linea_cercana(img, x1, y1, x2, y2)
        if linea_ajustada:
            lineas_ajustadas.append(list(linea_ajustada))
        else:
            lineas_ajustadas.append([x1, y1, x2, y2])

    return jsonify({"lineas_ajustadas": lineas_ajustadas})

if __name__ == "__main__":
    app.run()