# app.py
# A simple Flask API to serve model predictions to the browser extension.

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", "")
    # For now, return a dummy prediction
    response = {"prediction": "real", "score": 0.85}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
