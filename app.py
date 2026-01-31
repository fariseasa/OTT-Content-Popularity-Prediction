import streamlit as st
import pandas as pd
import joblib

# Load files
model = joblib.load("ott_popularity_model.pkl")
model_columns = joblib.load("model_columns.pkl")
categories = joblib.load("categories.pkl")

st.title("🎬 OTT Popularity Predictor")

st.header("Enter Movie Details")

year = st.number_input("Year", 1950, 2025, 2003)
runtime = st.number_input("Runtime (Minutes)", 1, 500, 50)

censor = st.selectbox("Censor Rating", categories["Censor"])
genre = st.selectbox("Main Genre", categories["main_genre"])

# Prediction
if st.button("Predict Popularity"):

    # Create empty dataframe
    input_df = pd.DataFrame([[0]*len(model_columns)], columns=model_columns)

    # Numeric values
    input_df["Year"] = year
    input_df["Runtime(Mins)"] = runtime

    # Dummy encoding
    censor_col = f"Censor_{censor}"
    genre_col = f"main_genre_{genre}"

    if censor_col in input_df.columns:
        input_df[censor_col] = 1

    if genre_col in input_df.columns:
        input_df[genre_col] = 1

    # Prediction
    prediction = model.predict(input_df)[0]

    result_map = {
        0: "Low Popularity 📉",
        1: "Medium Popularity 📊",
        2: "High Popularity 🔥"
    }

    st.success(result_map[prediction])