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
