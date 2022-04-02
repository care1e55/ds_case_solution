from pathlib import Path
import typer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

app = typer.Typer()


class Pipeline:

    def __init__(self, *args, **kwargs):
        self.model = GradientBoostingRegressor(*args, **kwargs)

    def _get_features(self, data):
        return data.drop(columns=['dteday', 'cnt'])

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
    data_path: Path = typer.Option('resources/data.csv'),
    test_size: float = typer.Option(0.25),
    random_state: int = typer.Option(42),
):
    data = pd.read_csv(data_path)
    data_train, data_test = train_test_split(data, test_size=test_size, random_state=random_state)
    pipeline = Pipeline(random_state=random_state)
    pipeline.fit(data_train)
    score = pipeline.score(data_test)
    typer.echo(f"The score is {score}")


if __name__ == '__main__':
    app()
