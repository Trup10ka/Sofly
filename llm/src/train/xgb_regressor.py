import time

from pandas import DataFrame
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


def train_xgb_regressor_with_scaler(sofa_frame: DataFrame):

    x = sofa_frame.iloc[:, :-1]
    y = sofa_frame.iloc[:, -1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.18, random_state=42)

    model = XGBRegressor(
        n_estimators=600,
        learning_rate=0.05,
        max_depth=4,
        colsample_bytree=0.8,
        subsample=0.8,
        reg_alpha=0.08,  # If you suspect irrelevant features, increase alpha to encourage sparsity.
        reg_lambda=0.20,  # If you want to smooth weights, increase lambda.
        random_state=42
    )

    time_taken_start = time.time()
    model.fit(x_train, y_train)
    print(str(time.time() - time_taken_start) + " seconds")

    y_pred = model.predict(x_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"XGB REGRESSOR | Mean Squared Error: {mse}")
    print(f"XGB REGRESSOR | Mean Absolute Error: {mae}")

    return model