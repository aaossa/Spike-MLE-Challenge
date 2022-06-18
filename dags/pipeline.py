from datetime import datetime
from pathlib import Path

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from utils.data_management import split_data
from utils.models import train_model
from utils.load_data import (
    load_rainfall_data, load_macroeconomic_data, load_milk_price_data,
)


default_args = {
    "owner": "Antonio Ossa Guerra",
    "email_on_failure": False,
    "email": ["aaossa@uc.cl"],
    "start_date": datetime(2022, 6, 17),
}

with DAG(
    "ml-pipeline",
    description="Data processing and model training pipeline",
    default_args=default_args,
    ) as dag:

    with TaskGroup("preprocess_data") as preprocess_data:
        preprocess_rainfall_data = PythonOperator(
            task_id="preprocess_rainfall_data",
            python_callable=load_rainfall_data,
            provide_context=True,
        )
        preprocess_macroeconomic_data = PythonOperator(
            task_id="preprocess_macroeconomic_data",
            python_callable=load_macroeconomic_data,
            provide_context=True,
        )

    preprocess_milk_price_data = PythonOperator(
        task_id="preprocess_milk_price_data",
        python_callable=load_milk_price_data,
        provide_context=True,
    )

    create_data_splits = PythonOperator(
        task_id="create_data_splits",
        python_callable=split_data,
        provide_context=True,
    )

    with TaskGroup("train_models") as train_models:
        train_model_1 = PythonOperator(
            task_id="train_model_1",
            python_callable=train_model,
            op_args=("model1",),
            op_kwargs={"verbose": 3},
            provide_context=True,
        )
        train_model_2 = PythonOperator(
            task_id="train_model_2",
            python_callable=train_model,
            op_args=("model2",),
            op_kwargs={
                "columns_criteria": lambda col: not "leche" in col,
                "verbose": 3,
            },
            provide_context=True,
        )

    stop_task = EmptyOperator(
        task_id="stop",
    )

    preprocess_data >> preprocess_milk_price_data >> create_data_splits >> train_models >> stop_task
