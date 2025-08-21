# app/streamlit_app.py

import streamlit as st
import requests
import base64

st.set_page_config(page_title="Milk Quality App", page_icon="🥛")
st.title("🥛 Milk Quality App")

# Create tabs
tab1, tab2 = st.tabs(["📊 Predict Quality", "📈 Visualize Input"])

# Shared input form
def input_form(key_prefix="form"):
    st.markdown("### Enter Milk Test Values")
    pH = st.slider("pH", 0.0, 14.0, 6.5, key=f"{key_prefix}_ph")
    temperature = st.slider("Temperature (°C)", 0.0, 100.0, 40.0, key=f"{key_prefix}_temperature")
    taste = st.selectbox("Taste", [1, 0], key=f"{key_prefix}_taste")
    odor = st.selectbox("Odor", [1, 0], key=f"{key_prefix}_odor")
    fat = st.selectbox("Fat", [1, 0], key=f"{key_prefix}_fat")
    turbidity = st.selectbox("Turbidity", [1, 0], key=f"{key_prefix}_turbidity")
    color = st.slider("Color", 1, 10, 4, key=f"{key_prefix}_color")
    return {
        "pH": pH,
        "Temperature": temperature,
        "Taste": taste,
        "Odor": odor,
        "Fat": fat,
        "Turbidity": turbidity,
        "Color": color
    }


# ---- Tab 1: Predict ----
with tab1:
    input_data = input_form(key_prefix="predict")
    if st.button("Predict Quality"):
        try:
            api_url = "http://localhost:8000/predict"
            response = requests.post(api_url, json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Predicted Milk Quality: **{result['predicted_quality']}**")
            else:
                st.error("Prediction failed.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ---- Tab 2: Visualize ----
# --- Tab 2: Visualization ---
with tab2:
    st.markdown("### 📈 Visualize a Feature")

    # User selects the type of plot
    plot_type = st.selectbox("Select Plot Type", ["Histogram", "Box Plot", "Violin Plot"], key="plot_type")
    
    # Then selects feature
    feature = st.selectbox("Select Feature to Plot", 
        ["pH", "Temprature", "Taste", "Odor", "Fat", "Turbidity", "Colour"],
        key="plot_feature"
    )

    if st.button("Generate Plot"):
        try:
            payload = {"feature": feature, "plot_type": plot_type}
            response = requests.post("http://localhost:8000/plot", json=payload)
            if response.status_code == 200:
                result = response.json()
                if "plot_base64" in result:
                    img = base64.b64decode(result["plot_base64"])
                    st.image(img, caption=f"{plot_type} of {feature}")
                else:
                    st.error(result.get("error", "Failed to render plot."))
            else:
                st.error("Failed to connect to the plot API.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
