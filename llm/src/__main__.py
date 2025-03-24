
import pandas as pd
from pandas import DataFrame

from src.train.gradient_boosting_regressor import train_gradient_boosting_regressor_with_scaler
from src.train.linear_regression import train_linear_regression
from src.train.random_forest_regressor import train_random_forest_regressor_with_scaler
from src.train.xgb_regressor import train_xgb_regressor_with_scaler
from src.util import map_non_numeric_columns


def remove_error_column_and_save(frame: DataFrame):
    frame.drop(columns=["ERROR"], inplace=True)
    # frame.to_csv("data/sofa-set.csv", index=False)

def remove_contains_metal_and_hardwood(frame: DataFrame):
    # frame.drop(columns=["contains_metal"], inplace=True)
    #frame.drop(columns=["contains_hardwood"], inplace=True)
    #frame.drop(columns=["cover_material"], inplace=True)
    pass

def main():
    loaded_sofa_csv = pd.read_csv("data/sofa-set.csv")
    remove_contains_metal_and_hardwood(loaded_sofa_csv)
    print(f"Number of entries: {len(loaded_sofa_csv)} before dropping duplicates")
    loaded_sofa_csv.drop_duplicates(inplace=True)
    print(f"Number of entries: {len(loaded_sofa_csv)} after dropping duplicates")

    #map_non_numeric_columns(loaded_sofa_csv)
    # gradient_boost_model = train_gradient_boosting_regressor_with_scaler(loaded_sofa_csv)
    # random_forest_model = train_random_forest_regressor_with_scaler(loaded_sofa_csv)
    # xgb_model = train_xgb_regressor_with_scaler(loaded_sofa_csv)
    linear_regression_model = train_linear_regression(loaded_sofa_csv)

    print(linear_regression_model.predict([
        [90,55,113,0,1,1]
    ]))


if __name__ == "__main__":
    main()