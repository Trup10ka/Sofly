import time

from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


def train_linear_regression(sofa_frame: DataFrame):

    x = sofa_frame.iloc[:, :-1]
    y = sofa_frame.iloc[:, -1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    model = LinearRegression()

    time_taken_start = time.time()
    model.fit(x_train, y_train)
    print(str(time.time() - time_taken_start) + " seconds")

    y_pred = model.predict(x_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"LINEAR REGRESSION | Mean Squared Error: {mse}")
    print(f"LINEAR REGRESSION | Mean Absolute Error: {mae}")

    return model