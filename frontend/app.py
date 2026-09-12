
import streamlit as st
import pandas as pd
import requests
import os

# The backend URL. Inside the Docker network the Flask service is reachable by its
# service name; override with the API_URL environment variable if needed.
API_URL = os.environ.get("API_URL", "http://backend:7860")

st.set_page_config(page_title="SuperKart Sales Predictor", page_icon="🛒")
st.title("🛒 SuperKart Product Sales Predictor")
st.write("Predict the total sales revenue of a product in a store.")

tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

# ---------------- Single (online) prediction ----------------
with tab1:
    st.subheader("Enter product and store details")

    product_weight = st.number_input("Product Weight", min_value=1.0, max_value=50.0, value=12.66)
    product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    product_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
    product_mrp = st.number_input("Product MRP", min_value=1.0, max_value=500.0, value=117.08)
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    store_city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
    product_id_char = st.selectbox("Product Id Category", ["FD", "DR", "NC"])
    store_est_year = st.number_input("Store Establishment Year", min_value=1980, max_value=2025, value=2009)
    product_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar,
            "Product_Allocated_Area": product_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_city,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": 2025 - store_est_year,
            "Product_Type_Category": product_cat,
        }
        try:
            resp = requests.post(f"{API_URL}/v1/predict", json=payload)
            resp.raise_for_status()
            st.success(f"Predicted Sales: {resp.json()['Predicted Sales']}")
        except Exception as e:
            st.error(f"Could not reach the prediction API: {e}")

# ---------------- Batch prediction ----------------
with tab2:
    st.subheader("Upload a CSV file for batch prediction")
    st.caption("The CSV must contain: Product_Weight, Product_Sugar_Content, Product_Allocated_Area, "
               "Product_MRP, Store_Size, Store_Location_City_Type, Store_Type, Product_Id_char, "
               "Store_Age_Years, Product_Type_Category")
    uploaded = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded is not None and st.button("Predict Batch"):
        try:
            files = {"file": uploaded.getvalue()}
            resp = requests.post(f"{API_URL}/v1/predictbatch", files=files)
            resp.raise_for_status()
            preds = resp.json()
            df_in = pd.read_csv(uploaded)
            df_in["Predicted_Sales"] = list(preds.values())
            st.dataframe(df_in)
        except Exception as e:
            st.error(f"Could not reach the prediction API: {e}")
