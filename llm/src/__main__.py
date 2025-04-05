import pickle
import re

import pandas as pd
from pandas import DataFrame

from llm.src.train.gradient_boosting_regressor import train_gradient_boosting_regressor_with_scaler
from llm.src.train.linear_regression import train_linear_regression
from llm.src.train.random_forest_regressor import train_random_forest_regressor_with_scaler
from llm.src.train.xgb_regressor import train_xgb_regressor_with_scaler


def remove_error_column_and_save(frame: DataFrame):
    frame.drop(columns=["ERROR"], inplace=True)

def export_models(*models: list[object]):
    for model in models:
        model_name = '_'.join([word.lower() for word in re.findall(r'[A-Z][a-z]*', model.__class__.__name__)])
        with open(f"llm/.export/{model_name}.llm.pkl", "wb") as file:
            pickle.dump(model, file)
        print(f"Model {model_name} saved successfully.")

def main():
    loaded_sofa_csv = pd.read_csv("llm/data/furniture_dataset.csv")
    remove_error_column_and_save(loaded_sofa_csv)
    print(f"Number of entries: {len(loaded_sofa_csv)} before dropping duplicates")
    loaded_sofa_csv.drop_duplicates(inplace=True)
    print(f"Number of entries: {len(loaded_sofa_csv)} after dropping duplicates")

    gradient_boost_model = train_gradient_boosting_regressor_with_scaler(loaded_sofa_csv)
    random_forest_model = train_random_forest_regressor_with_scaler(loaded_sofa_csv)
    xgb_model = train_xgb_regressor_with_scaler(loaded_sofa_csv)
    linear_regression_model = train_linear_regression(loaded_sofa_csv)

    export_models(gradient_boost_model, random_forest_model, xgb_model, linear_regression_model)

if __name__ == "__main__":
    main()