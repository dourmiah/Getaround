import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import joblib
import pandas as pd

app = FastAPI()

# Chargement du modèle
with open('regressor_model.pkl', 'rb') as file:
    loaded_model = joblib.load(file)

# Chargement du pipeline de preprocessing
with open('preprocessor_model.pkl', 'rb') as file:
    loaded_preprocessor = pickle.load(file)

class PredictionFeatures(BaseModel):
    input: list
    


@app.post('/predict')
async def predict(predictionfeatures: PredictionFeatures):
    """
    Prédiction du prix optimum de location pour un véhicule
    """
    input_data = predictionfeatures.input
    input_features = [
            "model_key",
            "mileage",
            "engine_power",
            "fuel",
            "paint_color",
            "car_type",
            "private_parking_available",
            "has_gps",
            "has_air_conditioning",
            "automatic_car",
            "has_getaround_connect",
            "has_speed_regulator",
            "winter_tires",
        ]
    df = pd.DataFrame(input_data, columns=input_features)
    data = loaded_preprocessor.transform(df)

    prediction = loaded_model.predict(data)

    response = {
        "Price": f"{prediction[0]:.2f} €"
    }

    return response

@app.get('/docs')
async def get_docs():
    return {"doc_url": "/docs"}


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)