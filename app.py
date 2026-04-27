import streamlit as st
import pandas as pd
import numpy as np
from heart_disease.utils.ml_utils.model.estimator import heart_disease_model
from heart_disease.utils.main_utils.utils import load_object


  
st.title("Heart Disease Prediction App")
st.write("This app predicts the likelihood of heart disease based on various health parameter .")
age=st.number_input('Age',min_value=1,max_value=120,value=30)
sex=st.selectbox('Sex', options=[0, 1], format_func=lambda x: 'Female' if x == 0 else 'Male')
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

trestbps=st.number_input('Resting Blood Pressure', min_value=0, value=120)
chol=st.number_input('Serum Cholesterol', min_value=0, value=200)
fbs=st.selectbox('Fasting Blood Sugar', options=[0, 1], format_func=lambda x: '<= 120 mg/dl' if x == 0 else '> 120 mg/dl')
restecg = st.selectbox(
    'Resting Electrocardiographic Results',
    options=[0, 1, 2],
    format_func=lambda x: {
        0: 'Normal',
        1: 'ST-T Wave Abnormality',
        2: 'Left Ventricular Hypertrophy'
    }[x]
)

thalach=st.number_input('Maximum Heart Rate Achieved', min_value=0, value=150)
exang=st.selectbox('Exercise Induced Angina', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
oldpeak=st.number_input('ST Depression Induced by Exercise', min_value=0.0, value=1.0)

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
if st.button('predict'):
    st.write("Predicting heart disease risk based on the input parameters ....")
    input_data=pd.DataFrame([{
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
    model=load_object("artifact/04_27_26_11_09_25/model_training/model.pkl")
    processor=load_object("artifact/04_27_26_11_09_25/data_transformation/transformed_object/processor.pkl")
    heart_disease_model_instance=load_object("artifact/04_27_26_11_09_25/model_training/model.pkl")
    prediction=heart_disease_model_instance.predict(input_data)
    if prediction[0]==1:
        st.error("the model predicts that you are at risk of heart disease. please cosult with a healthcare professonal for a comprehensive evaluation and personalized advice.")
    else:
        st.success("the model predicts that you are not at risk of heart disease. however it is important to maintain a healthy lifestyle and consult with a healthcare professional for regular check-ups and personalized advice.")

    