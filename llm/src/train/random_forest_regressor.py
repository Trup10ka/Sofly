import time

from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def train_random_forest_regressor_with_scaler(sofa_frame: DataFrame):

    x = sofa_frame.iloc[:, :-1]
    y = sofa_frame.iloc[:, -1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.23, random_state=42)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = RandomForestRegressor(
        n_estimators=500,  # More trees
        max_depth=12,  # Slightly deeper trees
        random_state=42
    )

    time_taken_start = time.time()
    model.fit(x_train_scaled, y_train)
    print(str(time.time() - time_taken_start) + " seconds")

    y_pred = model.predict(x_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"RANDOM FOREST REGRESSOR | Mean Squared Error: {mse}")
    print(f"RANDOM FOREST REGRESSOR | Mean Absolute Error: {mae}")

    return model