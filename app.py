import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Weather Forecast Prediction",
    page_icon="🌦️",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.stApp {
    background-color: #0E1117;
}

h1,h2,h3,h4,h5,h6 {
    color: white;
}

div[data-testid="stMetric"] {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 15px;
}

.prediction-box {
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:25px;
    font-weight:bold;
}

.success-box {
    background-color:#0f5132;
    color:white;
}

.danger-box {
    background-color:#842029;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD FILES
# -------------------------------------------------

scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("🌦️ Weather Forecast App")

model_option = st.sidebar.selectbox(
    "Select Prediction Model",
    [
        "Best Model",
        "Logistic Regression",
        "Decision Tree",
        "SVM",
        "Random Forest",
        "XGBoost"
    ]
)

# -------------------------------------------------
# MODEL LOADING
# -------------------------------------------------

if model_option == "Best Model":
    model = joblib.load("best_model.pkl")

elif model_option == "Logistic Regression":
    model = joblib.load("logistic_regression.pkl")

elif model_option == "Decision Tree":
    model = joblib.load("decision_tree.pkl")

elif model_option == "SVM":
    model = joblib.load("svm.pkl")

elif model_option == "Random Forest":
    model = joblib.load("random_forest.pkl")

elif model_option == "XGBoost":
    model = joblib.load("xgboost.pkl")

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🌦️ Weather Forecast Prediction System")

st.markdown("""
Predict whether it will rain based on weather conditions using
Machine Learning models.
""")

# -------------------------------------------------
# MODEL INFO
# -------------------------------------------------

st.info(f"🤖 Current Model: **{model_option}**")

# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------

st.subheader("📥 Enter Weather Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-20.0,
        max_value=60.0,
        value=25.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0
    )

with col2:
    wind_speed = st.number_input(
        "Wind Speed (km/h)",
        min_value=0.0,
        max_value=150.0,
        value=10.0
    )

    pressure = st.number_input(
        "Pressure (hPa)",
        min_value=800.0,
        max_value=1200.0,
        value=1013.0
    )

with col3:
    cloud_cover = st.number_input(
        "Cloud Cover (%)",
        min_value=0.0,
        max_value=100.0,
        value=40.0
    )

    # uv_index = st.number_input(
    #     "UV Index",
    #     min_value=0.0,
    #     max_value=15.0,
    #     value=5.0
    # )

# -------------------------------------------------
# DYNAMIC INPUTS
# -------------------------------------------------

st.subheader("⚙️ Remaining Features")

user_inputs = {}

for col in columns:

    if col.lower() in [
        "temperature",
        "humidity",
        "wind_speed",
        "pressure",
        "cloud_cover"
        # "uv_index"
    ]:
        continue

    user_inputs[col] = st.number_input(
        col.replace("_", " ").title(),
        value=0.0
    )

# -------------------------------------------------
# PREDICT BUTTON
# -------------------------------------------------

if st.button("🔍 Predict Weather", use_container_width=True):

    try:

        data = {}

        for col in columns:

            if col.lower() == "temperature":
                data[col] = temperature

            elif col.lower() == "humidity":
                data[col] = humidity

            elif col.lower() == "wind_speed":
                data[col] = wind_speed

            elif col.lower() == "pressure":
                data[col] = pressure

            elif col.lower() == "cloud_cover":
                data[col] = cloud_cover

            # elif col.lower() == "uv_index":
            #     data[col] = uv_index

            else:
                data[col] = user_inputs[col]

        input_df = pd.DataFrame([data])

        scaled_input = scaler.transform(input_df)

        prediction = model.predict(scaled_input)[0]

        st.divider()

        st.subheader("📊 Prediction Result")

        if prediction == 1:

            st.markdown(
                """
                <div class="prediction-box success-box">
                🌧️ RAIN EXPECTED
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="prediction-box danger-box">
                ☀️ NO RAIN EXPECTED
                </div>
                """,
                unsafe_allow_html=True
            )

        # Probability

        if hasattr(model, "predict_proba"):

            probability = model.predict_proba(scaled_input)

            confidence = np.max(probability) * 100

            st.metric(
                "Prediction Confidence",
                f"{confidence:.2f}%"
            )

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.markdown("""
### 🚀 About Project

This Weather Forecast Prediction System uses multiple Machine Learning algorithms:

- Logistic Regression
- Decision Tree
- SVM
- Random Forest
- XGBoost
- Best Model Selection

Users can compare predictions from different models and evaluate performance.

Developed using:
- Python
- Scikit-Learn
- XGBoost
- Streamlit
""")
