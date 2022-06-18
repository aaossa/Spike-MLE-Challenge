from sklearn.model_selection import train_test_split

from .utils import load_dataframe, save_dataframe


def split_data(dag_run=None, **kwargs):
    df, *_ = load_dataframe("df", src=dag_run.conf.get("tmp_path"))

    X = df.drop(["Precio_leche"], axis=1)
    y = df["Precio_leche"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
    )

    X_train.name = "X_train"
    X_test.name = "X_test"
    y_train.name = "y_train"
    y_test.name = "y_test"
    save_dataframe(X_train, X_test, y_train, y_test, dst=dag_run.conf.get("tmp_path"))
