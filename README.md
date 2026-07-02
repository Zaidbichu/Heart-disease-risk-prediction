# Heart-disease-risk-prediction
Machine learning project for predicting Heart disease risk using modular data pipelines, preprocessing, validation, and model evaluation.

# Heart Disease Risk Prediction

This project predicts the likelihood of heart disease using machine learning on structured healthcare data. It follows a modular pipeline-based architecture covering data ingestion, validation, transformation, model training, prediction, and deployment.

## Project Overview

The main goal of this project is to build an end-to-end machine learning system for heart disease prediction. The system takes patient health attributes as input and predicts whether the patient is at risk of heart disease.

## Features

- Modular ML pipeline architecture
- Data ingestion and train-test split
- Data validation using schema checks and drift detection
- Data transformation using scaling and encoding
- Model training with multiple classification algorithms
- Hyperparameter tuning
- Prediction pipeline for inference
- Streamlit app for deployment

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- YAML

## Dataset

The project uses a heart disease dataset derived from the UCI Heart Disease dataset.

Main features used:
- age
- sex
- cp
- trestbps
- chol
- fbs
- restecg
- thalach
- exang
- oldpeak
- slope
- ca
- thal

Target:
- `target_binary`

## Project Structure

```text
heart_disease/
├── components/
│   ├── data_ingestion.py
│   ├── data_validation.py
│   ├── data_transformation.py
│   └── model_training.py
├── entity/
│   ├── config_entity.py
│   └── artifact_entity.py
├── constants/
├── utils/
├── prediction_pipeline/
├── pipeline/
├── logging/
└── exception/
