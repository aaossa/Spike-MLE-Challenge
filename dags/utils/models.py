import numpy as np
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from .utils import load_dataframe, save_model


K = [3, 4, 5, 6, 7, 10]
ALPHA = [1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
POLY = [1, 2, 3, 5, 7]


def train_model(model_name, columns_criteria=None, verbose=0, dag_run=None, **kwargs):
    X_train, y_train = load_dataframe("X_train", "y_train", src=dag_run.conf.get("tmp_path"))

    if columns_criteria:
        columns = [col for col in X_train.columns if columns_criteria(col)]
        X_train = X_train[columns]

    np.random.seed(0)
    pipeline = Pipeline([
        ("scale", StandardScaler()),
        ("selector", SelectKBest(mutual_info_regression)),
        ("poly", PolynomialFeatures()),
        ("model", Ridge()),
    ])
    grid = GridSearchCV(
        estimator=pipeline,
        param_grid=dict(selector__k=K, poly__degree=POLY, model__alpha=ALPHA),
        cv=3, verbose=verbose, scoring="r2",
    )
    grid.fit(X_train, y_train)

    save_model(model_name, grid, dst=dag_run.conf.get("tmp_path"))
