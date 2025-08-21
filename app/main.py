
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os
from app.visualization import generate_plot

app = FastAPI(title="Milk Quality Prediction API")

# Load trained model
model = joblib.load("models/model.pkl")

# Load label encoder (if it exists)
encoder_path = "models/label_encoder.pkl"
label_encoder = joblib.load(encoder_path) if os.path.exists(encoder_path) else None

# Input schema using Pydantic
class MilkData(BaseModel):
    pH: float
    Temperature: float
    Taste: int
    Odor: int
    Fat: int
    Turbidity: int
    Color: int

# Request schema for plot
class PlotRequest(BaseModel):
    feature: str
    plot_type: str  # e.g., "Histogram", "Box Plot", "Violin Plot"
    
@app.get("/")
def root():
    return {"message": "Milk Quality Prediction API is live."}

@app.post("/predict")
def predict(data: MilkData):
    try:
        features = np.array([[data.pH, data.Temperature, data.Taste, data.Odor,
                              data.Fat, data.Turbidity, data.Color]])
        prediction = model.predict(features)[0]

        if label_encoder:
            prediction = label_encoder.inverse_transform([prediction])[0]

        return {"predicted_quality": str(prediction)}

    except Exception as e:
        return {"error": str(e)}



@app.post("/plot")
def plot(data: PlotRequest):
    try:
        img_base64 = generate_plot(feature=data.feature, plot_type=data.plot_type)
        if not img_base64:
            return {"error": "Invalid plot type"}
        return {"plot_base64": img_base64}
    except Exception as e:
        return {"error": str(e)}