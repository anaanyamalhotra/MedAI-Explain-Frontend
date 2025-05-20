import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="🧠 MedAI Explain", layout="centered")
st.title("🧠 MedAI Explain – Diabetes Risk Predictor")

tabs = st.tabs(["📝 Risk Test", "📊 Insights", "📥 Downloads", "ℹ️ About"])

with tabs[0]:
    with st.form("risk_form"):
        st.subheader("Enter Patient Information")
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

        backend_url = st.secrets["BACKEND_URL"]

        try:
            pred_resp = requests.post(f"{backend_url}/predict", json=input_data)
            pred_resp.raise_for_status()
            result = pred_resp.json()
            prob = result["probability"]
            risk_level = ("🔴 High Risk", "🟠 Moderate Risk", "🟢 Low Risk")[0 if prob >= 0.75 else 1 if prob >= 0.5 else 2]

            st.markdown(f"### 🧪 **Prediction**: {'Diabetic' if result['prediction'] == 1 else 'Non-Diabetic'}")
            st.markdown(f"### 📊 **Risk Probability**: {prob * 100:.1f}%")
            st.success(f"**Risk Category**: {risk_level}")

            # Feature Contribution (mock bar chart)
            st.subheader("🔍 Feature Contributions (Relative)")
            contributions = {
                "Glucose": Glucose / 200,
                "BMI": BMI / 50,
                "Insulin": Insulin / 300,
                "Age": Age / 100
            }
            contrib_df = pd.DataFrame(contributions.items(), columns=["Feature", "Importance"])
            fig = px.bar(contrib_df, x="Importance", y="Feature", orientation="h", color="Importance", height=300)
            st.plotly_chart(fig, use_container_width=True)

            # GPT-like explanation
            exp_resp = requests.post(f"{backend_url}/explain", json=input_data)
            explanation = exp_resp.json()["explanation"]
            st.subheader("💬 Explanation")
            st.write(explanation)

            # Health tips
            st.subheader("💡 Personalized Health Tips")
            tips = []
            if Glucose > 150: tips.append("➤ Reduce sugar intake and monitor glucose.")
            if BMI > 30: tips.append("➤ Increase physical activity to manage BMI.")
            if Insulin < 50: tips.append("➤ Consult your doctor about insulin resistance.")
            if Age > 45: tips.append("➤ Consider regular health screenings.")
            if not tips:
                tips.append("✅ All inputs look within healthy range. Keep up the good work!")

            for t in tips: st.markdown(t)

            # Store result for download tab
            st.session_state["latest_result"] = {
                **input_data,
                "Prediction": result["prediction"],
                "Probability": prob
            }

        except Exception as e:
            st.error("Something went wrong connecting to the backend.")
            st.text(str(e))

with tabs[1]:
    st.subheader("📊 Insights")
    st.write("Visual explanations of your results are in the Risk Test tab.")

with tabs[2]:
    st.subheader("📥 Download Your Results")
    if "latest_result" in st.session_state:
        df_out = pd.DataFrame([st.session_state["latest_result"]])
        st.download_button("📄 Download as CSV", data=df_out.to_csv(index=False),
                           file_name="medai_result.csv", mime="text/csv")
    else:
        st.info("Run a prediction first to enable downloads.")

with tabs[3]:
    st.subheader("ℹ️ About MedAI Explain")
    st.markdown(\"\"\"
**MedAI Explain** is an AI-powered tool that helps users assess their risk of Type 2 Diabetes 
using medical indicators and provides natural-language explanations and health tips.

Built with ❤️ using FastAPI, Streamlit, scikit-learn, and GPT-style explanation logic.
\"\"\")


    except Exception as e:
        st.error("Something went wrong connecting to the backend.")
        st.text(str(e))
