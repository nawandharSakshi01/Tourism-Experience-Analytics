# ============================================================
# TOURISM EXPERIENCE ANALYTICS
# Classification, Prediction & Recommendation System
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import os
import sqlite3

# Page configuration
st.set_page_config(
    page_title="Tourism Experience Analytics",
    page_icon="🌍",
    layout="wide"
)

# Main title
st.title("🌍 Tourism Experience Analytics")
st.subheader("Classification, Prediction & Recommendation System")

st.write(
    "This application predicts the visitor's travel mode "
    "and recommends attractions based on tourism data."
)

# ============================================================
# LOAD SAVED MODELS AND DATA
# ============================================================

# Path to the Models folder
models_path = "Models"

# Load classification model
classification_model = joblib.load(
    os.path.join(models_path, "classification_model.pkl")
)

# Load regression model
regression_model = joblib.load(
    os.path.join(models_path, "regression_model.pkl")
)

# Load recommendation data
attraction_data = joblib.load(
    os.path.join(models_path, "attraction_data.pkl")
)

# Load similarity matrix
similarity_matrix = joblib.load(
    os.path.join(models_path, "similarity_matrix.pkl")
)

# Load TF-IDF vectorizer
tfidf = joblib.load(
    os.path.join(models_path, "tfidf_vectorizer.pkl")
)

st.success("Models loaded successfully!")

# ============================================================
# VISIT MODE PREDICTION
# ============================================================

st.header("🎯 Predict Visitor's Visit Mode")

st.write(
    "Enter the visitor and attraction details to predict "
    "the most likely visit mode."
)

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    visit_year = st.selectbox(
        "Visit Year",
        list(range(2013, 2023))
    )

    visit_month = st.selectbox(
        "Visit Month",
        list(range(1, 13))
    )

    user_continent = st.text_input(
        "User Continent",
        value="Asia"
    )

    user_region = st.text_input(
        "User Region",
        value="Southern Asia"
    )

    user_country = st.text_input(
        "User Country",
        value="India"
    )

with col2:
    user_city = st.text_input(
        "User City",
        value="Unknown"
    )

    attraction_name = st.selectbox(
        "Attraction",
        sorted(attraction_data["Attraction"].dropna().unique())
    )

    selected_attraction = attraction_data[
        attraction_data["Attraction"] == attraction_name
    ].iloc[0]

    attraction_type = selected_attraction["AttractionType"]

    st.text_input(
        "Attraction Type",
        value=attraction_type,
        disabled=True
    )

    attraction_city = st.text_input(
        "Attraction City",
        value="Unknown"
    )

# Prediction button
if st.button("🔮 Predict Visit Mode"):

    # Prepare input data in the same format used during training
    input_data = pd.DataFrame({
        "VisitYear": [visit_year],
        "VisitMonth": [visit_month],
        "UserContinent": [user_continent],
        "UserRegion": [user_region],
        "UserCountry": [user_country],
        "UserCityName": [user_city],
        "Attraction": [attraction_name],
        "AttractionType": [attraction_type],
        "AttractionCityName": [attraction_city]
    })

    # Make prediction
    prediction = classification_model.predict(input_data)[0]

    st.success(f"🎉 Predicted Visit Mode: **{prediction}**")

    # ============================================================
# ATTRACTION RECOMMENDATION SYSTEM
# ============================================================

st.header("🌟 Recommended Attractions")

st.write(
    "Get similar attractions based on attraction type, "
    "location information, and average visitor ratings."
)

# Recommendation button
if st.button("✨ Get Recommendations"):

    # Get the selected attraction's index
    matching_indices = attraction_data[
        attraction_data["Attraction"].str.lower() == attraction_name.lower()
    ].index

    if len(matching_indices) == 0:
        st.error("Attraction not found.")

    else:
        idx = matching_indices[0]

        # Get similarity scores
        similarity_scores = list(
            enumerate(similarity_matrix[idx])
        )

        # Remove the selected attraction itself
        similarity_scores = [
            item for item in similarity_scores
            if item[0] != idx
        ]

        # Create recommendation dataframe
        recommendation_indices = [
            item[0] for item in similarity_scores
        ]

        recommendations = attraction_data.iloc[
            recommendation_indices
        ].copy()

        # Add similarity score
        score_lookup = dict(similarity_scores)

        recommendations["SimilarityScore"] = (
            recommendations.index.map(score_lookup)
        )

        # Normalize rating from 0–5 to 0–1
        recommendations["RatingScore"] = (
            recommendations["AverageRating"] / 5
        )

        # Final recommendation score
        recommendations["RecommendationScore"] = (
            0.7 * recommendations["SimilarityScore"]
            + 0.3 * recommendations["RatingScore"]
        )

        # Sort recommendations
        recommendations = recommendations.sort_values(
            by="RecommendationScore",
            ascending=False
        ).head(5)

        # Display recommendations
        st.success("Here are your top 5 recommended attractions:")

        st.dataframe(
            recommendations[
                [
                    "Attraction",
                    "AttractionType",
                    "AverageRating",
                    "RatingCount",
                    "RecommendationScore"
                ]
            ].reset_index(drop=True),
            use_container_width=True
        )

# ============================================================
# TOURISM ANALYTICS DASHBOARD
# ============================================================

st.header("📊 Tourism Analytics Dashboard")

st.write(
    "Explore visitor patterns, ratings, and attraction popularity."
)

# Load tourism data from SQL database
conn = sqlite3.connect("SQL/tourism_analytics.db")

tourism_data = pd.read_sql_query(
    "SELECT * FROM tourism_data",
    conn
)

conn.close()

# ------------------------------------------------------------
# 1. Visit Mode Distribution
# ------------------------------------------------------------

st.subheader("👥 Visitor Distribution by Visit Mode")

visit_mode_counts = (
    tourism_data["VisitMode"]
    .value_counts()
    .reset_index()
)

visit_mode_counts.columns = ["VisitMode", "VisitorCount"]

st.bar_chart(
    visit_mode_counts.set_index("VisitMode")
)


# ------------------------------------------------------------
# 2. Rating Distribution
# ------------------------------------------------------------

st.subheader("⭐ Rating Distribution")

rating_counts = (
    tourism_data["Rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_counts.columns = ["Rating", "Count"]

st.bar_chart(
    rating_counts.set_index("Rating")
)


# ------------------------------------------------------------
# 3. Top 10 Attractions
# ------------------------------------------------------------

st.subheader("🏆 Top 10 Most Visited Attractions")

top_attractions = (
    tourism_data["Attraction"]
    .value_counts()
    .head(10)
    .sort_values(ascending=True)
)

st.bar_chart(top_attractions)


# ------------------------------------------------------------
# 4. Average Rating by Visit Mode
# ------------------------------------------------------------

st.subheader("⭐ Average Rating by Visit Mode")

avg_rating_mode = (
    tourism_data.groupby("VisitMode")["Rating"]
    .mean()
    .round(2)
    .sort_values(ascending=True)
)

st.bar_chart(avg_rating_mode)

# ============================================================
# RATING PREDICTION
# ============================================================

st.header("⭐ Predict Attraction Rating")

st.write(
    "Predict the expected rating for the selected attraction "
    "using visitor and attraction information."
)

if st.button("⭐ Predict Rating"):

    # Use the selected attraction's existing historical information
    selected_data = attraction_data[
        attraction_data["Attraction"] == attraction_name
    ].iloc[0]

    # Use predicted visit mode from the classification model
    predicted_visit_mode = classification_model.predict(
        pd.DataFrame({
            "VisitYear": [visit_year],
            "VisitMonth": [visit_month],
            "UserContinent": [user_continent],
            "UserRegion": [user_region],
            "UserCountry": [user_country],
            "UserCityName": [user_city],
            "Attraction": [attraction_name],
            "AttractionType": [attraction_type],
            "AttractionCityName": [attraction_city]
        })
    )[0]

    # Overall average rating is used when individual user
    # rating history is not available in the app
    user_avg_rating = tourism_data["Rating"].mean()

    # Attraction-specific historical features
    attraction_avg_rating = selected_data["AverageRating"]
    attraction_rating_count = selected_data["RatingCount"]

    # Prepare input for regression model
    rating_input = pd.DataFrame({
        "VisitYear": [visit_year],
        "VisitMonth": [visit_month],
        "VisitMode": [predicted_visit_mode],
        "UserContinent": [user_continent],
        "UserRegion": [user_region],
        "Attraction": [attraction_name],
        "AttractionType": [attraction_type],
        "UserAvgRating": [user_avg_rating],
        "AttractionAvgRating": [attraction_avg_rating],
        "AttractionRatingCount": [attraction_rating_count]
    })

    # Predict rating
    predicted_rating = regression_model.predict(rating_input)[0]

    # Keep rating within the valid 1–5 range
    predicted_rating = max(1, min(5, predicted_rating))

    st.success(
        f"⭐ Predicted Rating: **{predicted_rating:.2f} / 5**"
    )

    st.info(
        f"Predicted Visit Mode used: **{predicted_visit_mode}**"
    )

# ============================================================
# SIDEBAR - PROJECT INFORMATION
# ============================================================

with st.sidebar:
    st.title("🌍 Tourism Analytics")

    st.write("### Project Modules")

    st.write("🎯 Visit Mode Prediction")
    st.write("⭐ Rating Prediction")
    st.write("🌟 Attraction Recommendation")
    st.write("📊 Tourism Analytics")
    st.write("🗄️ SQL Analytics")

    st.divider()

    st.write("### Dataset Information")
    st.write("📌 Total Transactions: 52,930")
    st.write("📌 Attractions: 30")
    st.write("📌 Visit Modes: 5")
    st.write("📌 Rating Scale: 1–5")

    st.divider()

    st.caption(
        "Tourism Experience Analytics "
        "using Machine Learning and Data Analytics"
    )

# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.header("📈 Model Performance")

st.write(
    "Performance metrics obtained during model evaluation."
)

# Create three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Classification Accuracy",
        "46.94%"
    )

with col2:
    st.metric(
        "Classification F1 Score",
        "46.11%"
    )

with col3:
    st.metric(
        "Regression MAE",
        "0.7352"
    )

# Additional regression metric
st.metric(
    "Regression R² Score",
    "-0.0882"
)

st.info(
    "The classification model predicts visitor VisitMode, "
    "while the regression model predicts the expected Rating."
)