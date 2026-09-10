# 🌍 Tourism Experience Analytics

### Classification, Prediction and Recommendation System

## 📌 Project Overview

Tourism Experience Analytics is a Data Science and Machine Learning project that analyzes tourism data to understand visitor behavior, attraction popularity and ratings.

The project uses Machine Learning, SQL and Streamlit to provide predictions, recommendations and useful tourism insights.

---

## 🎯 Objectives

- Clean and preprocess tourism data.
- Perform Exploratory Data Analysis (EDA).
- Analyze visitor and attraction patterns.
- Predict visitor **Visit Mode** using Machine Learning.
- Predict **Attraction Rating**.
- Recommend similar attractions.
- Perform tourism analysis using SQL.
- Deploy the project using Streamlit.

---

## 📊 Dataset

The project uses tourism data containing information about:

- Users
- Attractions
- Cities
- Countries
- Regions
- Continents
- Visit Modes
- Ratings
- Transactions

**Total Transactions:** 52,930  
**Attractions:** 30  
**Visit Modes:** 5  
**Rating Scale:** 1–5

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- SQL
- SQLite
- Streamlit
- Joblib

---

## 🤖 Machine Learning

### Classification

A **Random Forest Classifier** is used to predict the visitor's Visit Mode.

Visit Modes:

- Business
- Couples
- Family
- Friends
- Solo

**Accuracy:** 46.94%  
**F1 Score:** 46.11%

### Regression

A **Random Forest Regressor** is used to predict attraction ratings.

**MAE:** 0.7352  
**R² Score:** -0.0882

### Recommendation System

A content-based recommendation system is implemented using:

- TF-IDF
- Cosine Similarity
- Attraction Rating

The recommendation score combines similarity and attraction rating.

---

## 📈 EDA Insights

Some important findings from the analysis:

- **Couples** have the highest number of visits.
- Ratings of **4 and 5** are the most common.
- **Water Parks** have the highest average rating among attraction types.
- **Sacred Monkey Forest Sanctuary** is the most visited attraction.
- Asia has the highest visitor count among the available continents.

---

## 🗄️ SQL Analysis

SQLite is used for tourism data analysis.

SQL queries are used to find:

- Top visited attractions
- Average attraction ratings
- Visit Mode distribution
- Average rating by Visit Mode
- Most popular attraction types

---

## 🌐 Streamlit Application

The project is deployed using Streamlit.

The application provides:

- Visit Mode prediction
- Rating prediction
- Attraction recommendations
- Tourism analytics dashboard
- Data visualizations

**Streamlit App:**  
[Open Tourism Experience Analytics App](http://10.175.104.248:8501/)

Author

Sakshi Nawandhar

B.Tech Computer Science Engineering
Jhulelal Institute of Technology, Nagpur

✅ Conclusion

This project provides an end-to-end tourism analytics solution using Data Science, Machine Learning, SQL and Streamlit.

It helps analyze tourism trends, predict visitor behavior and ratings, and recommend suitable attractions.
> Note: This is a local network address and may not be accessible outside the network where the application is running.

---
