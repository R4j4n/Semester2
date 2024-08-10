import torch
import pandas as pd
import torch.nn as nn
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler


class StudentNeuralNet(nn.Module):
    def __init__(self, input_dim):
        super(StudentNeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x


class GetTransformer:

    def __init__(self, dataframe: None = None) -> None:

        if dataframe:
            self.dataframe = dataframe
        else:
            self.dataframe = pd.read_csv("static/cleaned.csv")
            self.dataframe.drop("Unnamed: 0", axis=1, inplace=True)

        self.nominal_variables = [
            "first_language",
            "funding",
            "school",
            "fast_track",
            "coop",
            "residency",
            "gender",
            "prev_education",
        ]

        self.ordinal_variables = ["age_group", "english_grade"]

        self.numerical_variables = [
            "first_term_gpa",
            "second_term_gpa",
            "high_school_average_mark",
            "math_score",
        ]

    def get_pipe(self):

        # Update the nominal and ordinal pipelines to handle unknown categories
        nominal_pipe = Pipeline(
            steps=[
                (
                    "onehot",
                    OneHotEncoder(
                        drop="first", sparse_output=False, handle_unknown="ignore"
                    ),
                )
            ]
        )

        ordinal_pipe = Pipeline(
            steps=[
                (
                    "ordinal",
                    OrdinalEncoder(
                        handle_unknown="use_encoded_value", unknown_value=-1
                    ),
                )
            ]
        )

        numerical_pipe = Pipeline(steps=[("scaler", MinMaxScaler())])

        preprocessor = ColumnTransformer(
            transformers=[
                ("nominal", nominal_pipe, self.nominal_variables),
                ("ordinal", ordinal_pipe, self.ordinal_variables),
                ("numerical", numerical_pipe, self.numerical_variables),
            ]
        )

        full_pipeline = Pipeline(steps=[("preprocessor", preprocessor)])

        # Apply the pipeline to the test data
        full_pipeline.fit_transform(self.dataframe)

        return full_pipeline
