from pandas import DataFrame
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def train_neutral_network_regressor(sofa_frame: DataFrame) -> Sequential:

    x = sofa_frame.iloc[:, :-1]
    y = sofa_frame.iloc[:, -1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    model = Sequential()

    model.add(Dense(80, activation='relu', input_shape=x_train.shape[1:]))
    model.add(Dense(60, activation='relu'))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mae'])
    model.fit(x_train, y_train, epochs=200, batch_size=64, verbose=1)

    return model


