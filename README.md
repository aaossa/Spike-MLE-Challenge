# Spike MLE Challenge

> Antonio Ossa Guerra (aaossa@uc.cl)

This repository reflects the development of my answer to the [Spike MLE Challenge](https://github.com/SpikeLab-CL/ml-engineer-challenge).


### Mounting the project

The project setup is part of a Docker container. To use its contents, run the following command:

```raw
docker-compose up --build
```


### Running the pipeline

Apache Airflow will be available at http://localhost:8080 (credentials are `airflow` as user and password). A single DAG will be available, representing the proposed processing pipeline.


### Querying the API

The trained models will be available for querying through a Flask API at the endpoing http://localhost:5000/predict by using the following parameters:

* `"query"`: Array of JSON objects with the column names of the input data and their corresponding values.
* `"model"`: (Optional) Model name, corresponding to the filename of the serialized model. 

Response:

* `"prediction"`: Array of integers where each number is the predicted value of the corresponding JSON object on `"query"`

Sample program to test the API:

```python
# api/demo.py
import requests


API_URL = "http://localhost:5000/predict"
data = [
  {
    "ano": 2014,
    "mes": 1,
    "Coquimbo": 3.5246732065,
    "Valparaiso": 2.3787662296,
    "Metropolitana_de_Santiago": 7.2782718104,
    ...
    "Imacec_no_minero": 97.5,
    "num": 94.3
  },
  {
    "ano": 2014,
    "mes": 2,
    "Coquimbo": 1.6888562116,
    "Valparaiso": 8.3898538959,
    "Metropolitana_de_Santiago": 17.8030704519,
    ...
    "Imacec_no_minero": 93.4,
    "num": 92.8
  }
]
model = "model1"  # Optional

if __name__ == '__main__':
    api_prediction = requests.post(API_URL, json={"query": data, "model": model})
    print(api_prediction)
    # {'prediction': [244.54084431277155, 171.87887865792788]}

```
