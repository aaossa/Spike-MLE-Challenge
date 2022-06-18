import json
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    query = pd.DataFrame(request.get_json().get("query"))
    model_name = request.get_json().get("model", "model1")
    model = joblib.load(f"{model_name}.joblib")
    pred = model.predict(query)
    return jsonify({"prediction": pred.flatten().tolist()})


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)
