from pathlib import Path

import numpy as np
import typer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

app = typer.Typer()


class Pipeline:

    def __init__(self, *args, **kwargs):
        self.model = GradientBoostingRegressor(*args, **kwargs)

    @staticmethod
    def encode_cyclic(data: pd.DataFrame, column: str) -> pd.Series:
        max_x = data[column].max()
        return data[column].apply(
            lambda x: np.cos(2 * np.pi * x / (max_x + 1))
        ).reset_index(drop=True)

    @staticmethod
    def encode_ordinal(data: pd.DataFrame, column: str) -> pd.DataFrame:
        return pd.DataFrame(OrdinalEncoder().fit_transform(
            data[column].values.reshape(data.shape[0], 1)
        ).astype(int))

    @staticmethod
    def encode_binary_onehot(data: pd.DataFrame, column: str) -> pd.DataFrame:
        return pd.get_dummies(data[column]).rename(columns={0: f'not_{column}', 1: column}).reset_index(drop=True)

    def _get_features(self, data):
        features = data[[
            'yr',
            'mnth',
            'weekday',
            'workingday',
            'holiday',
            'hum',
            'temp',
            'windspeed',
        ]]
        encoded_weekdays = self.encode_cyclic(features, 'weekday')
        encoded_holiday = self.encode_binary_onehot(features, 'holiday')
        encoded_workingday = self.encode_binary_onehot(features, 'workingday')
        encoded_mnth = self.encode_ordinal(features, 'mnth')
        features = pd.concat(
            (
                 features.drop(['holiday', 'workingday', 'mnth', 'weekday'], axis=1).reset_index(drop=True),
                 encoded_weekdays,
                 encoded_holiday,
                 encoded_workingday,
                 encoded_mnth
            ), axis=1)
        return features

    def _get_target(self, data):
        return data['cnt']

    def fit(self, data):
        X, y = self._get_features(data), self._get_target(data)
        self.model.fit(X, y)
        return self

    def predict(self, data):
        X = self._get_features(data)
        return self.model.predict(X)

    def score(self, data):
        X = self._get_features(data)
        target = self._get_target(data)
        return self.model.score(X, target)


@app.command()
def evaluate(
    data_path: Path = typer.Option(...),
    test_size: float = typer.Option(0.25),
    random_state: int = typer.Option(42),
):
    data = pd.read_csv(data_path)
    data_train, data_test = train_test_split(data, test_size=test_size, random_state=random_state)
    pipeline = Pipeline(random_state=random_state)
    pipeline.fit(data_train)
    score = pipeline.score(data_test)
    typer.echo(f"The R^2 score is {score}")


if __name__ == '__main__':
    app()
