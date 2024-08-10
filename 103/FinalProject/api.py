import joblib
import torch
import uvicorn
import pandas as pd
from fastapi import FastAPI, HTTPException

from utils import StudentNeuralNet, GetTransformer

################### Data Model ###################
from pydantic import BaseModel, Field


class Details(BaseModel):

    first_language: int = Field(..., example=3)
    funding: int = Field(..., example=4)
    school: int = Field(..., example=6)
    fast_track: int = Field(..., example=1)
    coop: int = Field(..., example=2)
    residency: int = Field(..., example=2)
    gender: int = Field(..., example=2)
    prev_education: int = Field(..., example=1)
    age_group: int = Field(..., example=3)
    english_grade: int = Field(..., example=7)
    first_term_gpa: float = Field(..., example=2.5)
    second_term_gpa: float = Field(..., example=2.0)
    high_school_average_mark: float = Field(..., example=73.28)
    math_score: float = Field(..., example=34.24)


# load the nerual network model
model = StudentNeuralNet(input_dim=20)
model.load_state_dict(torch.load("model.pth"))


# load the data transformer
transformer = GetTransformer()
pipeline = transformer.get_pipe()


app = FastAPI()

origins = ["*"]


@app.post("/predict/firstyearpersistence/")
async def generate_and_execute(data: Details):

    # convert pydantic to dict
    data_dict = data.model_dump()

    # create a dataframe from the dicitonary
    df = pd.DataFrame([data_dict])  # Create a DataFrame from the dictionary

    try:
        # convert the data into training data format
        processed_test_data = pipeline.transform(df)

        # set the model to evaluation
        model.eval()

        # convert the data into pytorch tensor
        X_train_tensor = torch.tensor(processed_test_data, dtype=torch.float32)

        opt = model(X_train_tensor)

        true_probability = opt.cpu().float().item()

        true_class = (opt > 0.5).float().item()

        prob_dist = []
        if int(true_class) == 1:
            prob_dist.append([1 - true_probability, true_probability])
        else:
            prob_dist.append([true_probability, 1 - true_probability])

        return {
            "probability": prob_dist,
            "class": true_class,
        }

    except:
        raise HTTPException(
            status_code=500, detail="Something happened! Cannot process the input."
        )


if __name__ == "__main__":

    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=2222)
