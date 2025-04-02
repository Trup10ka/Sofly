import time

from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

def train_gradient_boosting_regressor_with_scaler(sofa_frame: DataFrame):

    x = sofa_frame.iloc[:, :-1]
    y = sofa_frame.iloc[:, -1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    model = GradientBoostingRegressor(
        n_estimators=700,  # More trees
        learning_rate=0.025,  # Smaller step sizes
        max_depth=25,  # Slightly deeper trees
        subsample=0.8,  # Reduce overfitting
        random_state=42
    )

    time_taken_start = time.time()
    model.fit(x_train, y_train)
    print(str(time.time() - time_taken_start) + " seconds")

    y_pred = model.predict(x_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"GRADIENT BOOSTER REGRESSOR | Mean Squared Error: {mse}")
    print(f"GRADIENT BOOSTER REGRESSOR | Mean Absolute Error: {mae}")

    return model