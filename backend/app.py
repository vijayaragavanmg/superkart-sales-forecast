
from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Predictor")

# Load the serialized model pipeline (preprocessing + model) once at startup
model = joblib.load("superkart_model.joblib")

# The exact feature columns the model expects (order does not matter for a DataFrame)
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
    "Product_MRP", "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]


@superkart_api.get("/")
def home():
    return "SuperKart Sales Prediction API is running. Use POST /v1/predict or /v1/predictbatch."


@superkart_api.post("/v1/predict")
def predict():
    """Online (single) inference from a JSON payload."""
    data = request.get_json()
    # Build a one-row DataFrame from the incoming JSON
    input_df = pd.DataFrame([data])[FEATURES]
    prediction = model.predict(input_df)[0]
    return jsonify({"Predicted Sales": round(float(prediction), 2)})


@superkart_api.post("/v1/predictbatch")
def predict_batch():
    """Batch inference from an uploaded CSV file (form field name: 'file')."""
    file = request.files["file"]
    input_df = pd.read_csv(file)[FEATURES]
    predictions = model.predict(input_df)
    output = {str(i): round(float(p), 2) for i, p in enumerate(predictions)}
    return jsonify(output)


if __name__ == "__main__":
    # 0.0.0.0 makes the API reachable from outside the container; port 7860 is forwarded
    superkart_api.run(host="0.0.0.0", port=7860)
