# Resume analysis using nachine learning to optimize recruitment processes

## Summary

This repository contains the full implementation and documentation of the master’s thesis prepared as part of the Machine Learning master's program at Warsaw University of Technology.

The purpose of this thesis was to develop and implement a system that enables the automatic review of candidates applying for specific job openings. The system uses modern natural language processing and machine learning technologies to support recruitment processes by automating the analysis of application documents. 

The work involved extracting data from application documents using a pretrained model with Named Entity Recognition (NER) techniques to identify candidates names. A pretrained BART model was also used to generate summaries of resume content, allowing for quick and clear representation of key candidate information, such as work experience or skills. In addition, a resume classification module based on the XGBoost model was implemented, which was pretrained on properly prepared data containing resumes and occupational category, achieving a classification accuracy of 79% with 24 classes. A custom neural network based on the LSTM architecture was developed to rank candidates in terms of matching job requirements. The model was trained on a dataset containing resumes, job offers and assignments to three classes: good fit, no fit and potential fit. The model achieved an accuracy of 83%.

The results indicate that the designed system effectively supports recruitment processes, speeding up the analysis of applications and improving the accuracy of candidate selection, making it a valuable tool in modern human resource management processes.

## Project Description

The project consists of two applications: **web** and **backend**, both run using Docker Compose.

## Prerequisites

- Docker (<https://docs.docker.com/get-docker/>)
- Docker Compose (<https://docs.docker.com/compose/>)

## Project Structure

```text
.
├── docker-compose.yml
├── web
│   └── frontend application code
├── experiments
│   ├── classification
│   │   └── experiment code – CV classification
│   └── ranking
│       └── experiment code – CV ranking
├── data
│   └── data for model training
└── backend
    └── backend application code
```

## Running the Project

```bash
docker compose up
```

## Accessing the Applications

- Web: <http://localhost:3000>  
- Backend: <http://localhost:5000>

## Stopping the Applications

```bash
Ctrl-C
```

## Removing the Applications

```bash
docker compose down
```
