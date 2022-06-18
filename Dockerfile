FROM apache/airflow:2.3.2

RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir joblib
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir pandas
