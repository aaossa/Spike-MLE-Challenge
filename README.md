# Spike MLE Challenge

> Antonio Ossa Guerra (aaossa@uc.cl)

This repository reflects the development of my answer to the [Spike MLE Challenge](https://github.com/SpikeLab-CL/ml-engineer-challenge).


### Mounting the project

The project setup is part of a Docker container. To use its contents, run the following command:

```raw
docker-compose up --build
```


### Running the pipeline

Apache Airflow will be available at https://localhost:8080 (credentials are `airflow` as user and password). A single DAG will be available, representing the proposed processing pipeline.


---

### Notes to reviewers

First of all, I loved the challenge. Even if it was not that complex at first, it was a nice opportunity for me to try and learn Apache Airflow to create the pipeline. I spent a lot of time trying to make it work inside a Docker container and when I was finally done, I did not have much time left to write the API. Fortunetely, I'm familiar with Flask so mounting that service, the endpoint and querying the models was not that hard, but that part was completed after the deadline (https://github.com/aaossa/Spike-MLE-Challenge/pull/4).

With a couple more hours of time, I would have tried to make sure that the repository structure made sense for others. For example, not all of the services are mounted at the same level (Apache Airflow is mounted at root level, but the API is a single folder of the repository). Also, the pipeline could be improved, but I'm not sure if the tasks are too atomic. I tried to translate the ideas of the Data Scientist directly from the notebook to the processing pipeline.

Anyways, thank you for the opportunity. It was a really fun exercise and I already learned a lot while working on this repository.
