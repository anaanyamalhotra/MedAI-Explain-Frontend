# 💻 MedAI Explain – LLM-Powered Diabetes Risk Explainer

This is the Streamlit UI for **MedAI Explain**, a diabetes risk prediction and explainability platform.
**Live Demo:** https://medai-explain-frontend.streamlit.app/

## 🔍 What It Does
- Allows users to enter personal health metrics
- Connects to FastAPI backend for prediction
- Displays risk score, category, and confidence level
- Generates bar charts of feature importance
- Offers personalized health tips based on input
- Supports CSV export and tabbed UI

## 🌐 Live Demo
[Try the app here](https://medai-explain.streamlit.app)

## ⚙️ Stack
- Streamlit
- Plotly
- REST API integration
- CSV export

## 📁 Features
- 🧠 Risk predictor form
- 📊 Feature contribution chart
- 💬 Natural language explanation
- 💡 GPT-style health tips
- 📥 CSV download support
- 🌈 Polished tab-based UI

## 🛠 Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Secrets Required
`.streamlit/secrets.toml` (or Streamlit Cloud secrets):
```toml
BACKEND_URL = "https://your-backend-url.onrender.com"
```
