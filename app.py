import streamlit as st
import requests

st.set_page_config(page_title="MedAI Explain", layout="centered")
st.title("🧠 MedAI Explain – Diabetes Risk Predictor")

# Streamlit form for input
with st.form("input_form"):
    st.subheader("Enter Patient Information:")
    Pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    Glucose = st.number_input("Glucose Level", 0.0, 300.0, 120.0)
    BloodPressure = st.number_input("Blood Pressure (mm Hg)", 0.0, 150.0, 70.0)
    SkinThickness = st.number_input("Skin Thickness (mm)", 0.0, 100.0, 20.0)
    Insulin = st.number_input("Insulin (mu U/ml)", 0.0, 900.0, 85.0)
    BMI = st.number_input("BMI", 0.0, 70.0, 28.0)
    DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
    Age = st.number_input("Age", 1, 120, 35)

    submitted = st.form_submit_button("Predict Risk")

if submitted:
    input_data = {
        "Pregnancies": Pregnancies,
        "Glucose": Glucose,
        "BloodPressure": BloodPressure,
        "SkinThickness": SkinThickness,
        "Insulin": Insulin,
        "BMI": BMI,
        "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
        "Age": Age
    }

    backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000")

    # Call /predict endpoint
    try:
        pred_resp = requests.post(f"{backend_url}/predict", json=input_data)
        pred_resp.raise_for_status()
        result = pred_resp.json()
        st.success(f"🩺 **Prediction:** {'Diabetic' if result['prediction'] == 1 else 'Non-Diabetic'}")
        st.info(f"📊 **Probability:** {result['probability'] * 100:.1f}%")

        # Call /explain endpoint
        exp_resp = requests.post(f"{backend_url}/explain", json=input_data)
        exp_resp.raise_for_status()
        explanation = exp_resp.json()["explanation"]
        st.subheader("💬 Explanation")
        st.write(explanation)

    except Exception as e:
        st.error("Something went wrong connecting to the backend.")
        st.text(str(e))
