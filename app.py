import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import joblib
import pickle
import warnings

# Ensure the repository root is on sys.path so local modules (if any) can be imported.
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

st.title("Heart Disease Prediction App")
st.write("This app predicts the likelihood of heart disease based on various health parameters.")

age = st.number_input('Age', min_value=1, max_value=120, value=30)
sex = st.selectbox('Sex', options=[0, 1], format_func=lambda x: 'Female' if x == 0 else 'Male')
cp = st.selectbox(
    'Chest Pain Type',
    options=[1, 2, 3, 4],
    format_func=lambda x: {
        1: 'Typical Angina',
        2: 'Atypical Angina',
        3: 'Non-anginal Pain',
        4: 'Asymptomatic'
    }[x]
)

trestbps = st.number_input('Resting Blood Pressure', min_value=0, value=120)
chol = st.number_input('Serum Cholesterol', min_value=0, value=200)
fbs = st.selectbox('Fasting Blood Sugar', options=[0, 1], format_func=lambda x: '<= 120 mg/dl' if x == 0 else '> 120 mg/dl')
restecg = st.selectbox(
    'Resting Electrocardiographic Results',
    options=[0, 1, 2],
    format_func=lambda x: {
        0: 'Normal',
        1: 'ST-T Wave Abnormality',
        2: 'Left Ventricular Hypertrophy'
    }[x]
)

thalach = st.number_input('Maximum Heart Rate Achieved', min_value=0, value=150)
exang = st.selectbox('Exercise Induced Angina', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
oldpeak = st.number_input('ST Depression Induced by Exercise', min_value=0.0, value=1.0)

slope = st.selectbox(
    'Slope of the Peak Exercise ST Segment',
    options=[1, 2, 3],
    format_func=lambda x: {
        1: 'Upsloping',
        2: 'Flat',
        3: 'Downsloping'
    }[x]
)

ca = st.selectbox(
    'Number of Major Vessels Colored by Fluoroscopy',
    options=[0, 1, 2, 3]
)

thal = st.selectbox(
    'Thalassemia',
    options=[3, 6, 7],
    format_func=lambda x: {
        3: 'Normal',
        6: 'Fixed Defect',
        7: 'Reversible Defect'
    }[x]
)


def load_object(path: str):
    """Load a pickled/joblib object from a repository-relative path.

    The function joins the path to the repository root (where app.py lives) before loading.
    Returns None and shows a Streamlit warning if the file is not found or fails to load.
    """
    full_path = os.path.join(ROOT, path)
    if not os.path.exists(full_path):
        st.warning(f"File not found: {full_path}")
        return None
    try:
        # Prefer joblib for sklearn artifacts
        return joblib.load(full_path)
    except Exception:
        try:
            with open(full_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            st.warning(f"Failed to load object from {full_path}: {e}")
            return None


if st.button('Predict'):
    st.write("Predicting heart disease risk based on the input parameters...")
    input_data = pd.DataFrame([{
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal
    }])

    model_path = "artifact/04_27_26_11_09_25/model_training/model.pkl"
    processor_path = "artifact/04_27_26_11_09_25/data_transformation/transformed_object/processor.pkl"

    model = load_object(model_path)
    processor = load_object(processor_path)

    if model is None:
        st.error("Model file not found or failed to load. Check the artifact path and ensure the model file is present in the repo or adjust the path.")
    else:
        # If there's a preprocessor, try to transform the inputs first
        X = input_data
        if processor is not None:
            try:
                X = processor.transform(input_data)
            except Exception as e:
                # If transformer expects a DataFrame with specific columns/order, warn and fall back to raw input
                st.warning(f"Processor transform failed, using raw inputs instead: {e}")
                X = input_data
        try:
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(X)[:, 1]
                risk = float(probs[0])
            else:
                pred = model.predict(X)
                # if model returns labels (0/1) convert to probability-like value
                risk = float(pred[0])

            st.subheader("Prediction")
            st.metric(label="Predicted risk (probability or label)", value=f"{risk:.2f}")
            if risk >= 0.5:
                st.error("High risk of heart disease (threshold 0.5). Please consult a healthcare professional for a comprehensive evaluation and personalized advice.")
            else:
                st.success("Lower risk of heart disease (threshold 0.5). Maintain a healthy lifestyle and consult a healthcare professional if you have concerns.")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
