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

> PS: When using the web interface, select "Trigger DAG w/ config" and pass the contents of `./dags/pipeline-config.json` as configuration JSON for the DAG to run. The configuration includes the path of a temporal folder, the output folder for the models, and the paths of the source data.


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


---

### Notes to reviewers

First of all, I loved the challenge. Even if it was not that complex at first, it was a nice opportunity for me to try and learn Apache Airflow to create the pipeline. I spent a lot of time trying to make it work inside a Docker container and when I was finally done, I did not have much time left to write the API. Fortunetely, I'm familiar with Flask so mounting that service, the endpoint and querying the models was not that hard, but that part was completed after the deadline (https://github.com/aaossa/Spike-MLE-Challenge/pull/4).

With a couple more hours of time, I would have tried to make sure that the repository structure made sense for others. For example, not all of the services are mounted at the same level (Apache Airflow is mounted at root level, but the API is a single folder of the repository). Also, the pipeline could be improved, but I'm not sure if the tasks are too atomic. I tried to translate the ideas of the Data Scientist directly from the notebook to the processing pipeline.

Anyways, thank you for the opportunity. It was a really fun exercise and I already learned a lot while working on this repository.
