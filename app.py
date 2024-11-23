import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns

# Data cleaning
df = pd.read_csv('digital_marketing_campaign_dataset.csv')

# Check for missing values and drop them
df = df.dropna()

# Check for duplicates and drop them
df = df.drop_duplicates()

# Remove irrelevant columns
df = df.drop(["AdvertisingPlatform", "AdvertisingTool"], axis=1)

st.set_page_config(page_title='Digital Marketing Campaign Analysis', initial_sidebar_state='expanded', layout='wide')
st.title("Conversion Data Analysis")

# Filters in the sidebar
st.sidebar.header("Filters")

# Filters for Age Range, Campaign Channel, Gender, and Income
age_min, age_max = st.sidebar.slider('Select Age Range', min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=(18, 65))

# Adding "All" option to Campaign Channel filter
campaign_channel = st.sidebar.selectbox('Select Campaign Channel', ['All'] + list(df['CampaignChannel'].unique()))
# Adding "All" option to Gender filter
gender = st.sidebar.selectbox('Select Gender', ['All'] + list(df['Gender'].unique()))
# Adding "All" option to Income Range filter
income_min, income_max = st.sidebar.slider('Select Income Range', min_value=int(df['Income'].min()), max_value=int(df['Income'].max()), value=(df['Income'].min(), df['Income'].max()))

# Apply filters
filtered_df = df[(df['Age'] >= age_min) & (df['Age'] <= age_max)]

# Apply filters for Campaign Channel and Gender only if not 'All'
if campaign_channel != 'All':
    filtered_df = filtered_df[filtered_df['CampaignChannel'] == campaign_channel]

if gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == gender]

filtered_df = filtered_df[(filtered_df['Income'] >= income_min) & (filtered_df['Income'] <= income_max)]

# KPIs - Display at the top horizontally
col1, col2, col3 = st.columns(3)
with col1:
    avg_ctr = filtered_df['ClickThroughRate'].mean()
    st.metric("Average CTR", f"{avg_ctr:.2f}")
with col2:
    avg_conversion_rate = filtered_df['ConversionRate'].mean()
    st.metric("Average Conversion Rate", f"{avg_conversion_rate:.2f}")
with col3:
    total_ad_spend = filtered_df['AdSpend'].sum()
    st.metric("Total Ad Spend (USD)", f"${total_ad_spend:,.2f}")

# Bar Charts & Line Charts in separate columns
col11, col12 = st.columns(2)

# First Column for Bar Chart: Conversion Rate by Income Bracket
with col11:
    st.subheader("Conversion by Income Bracket")
    income_brackets = pd.cut(filtered_df['Income'], bins=[0, 30000, 60000, 90000, 120000, 150000], labels=["<30k", "30k-60k", "60k-90k", "90k-120k", "120k+"])
    conversion_by_income = filtered_df.groupby(income_brackets)['ConversionRate'].sum()  # Fixed reference to 'ConversionRate'
    st.bar_chart(conversion_by_income)
    
    # Simple Area Chart: Time Spent vs Conversion Rate
    st.subheader("Time Spent vs Conversion Rate")
    time_conversion = filtered_df.groupby('TimeOnSite')['ConversionRate'].mean()
    st.area_chart(time_conversion)

# Second Column for Bar Chart: Conversion by Income Bracket and other charts
with col12:
    st.subheader("Age vs Conversion Rate")
    age_conversion = filtered_df.groupby('Age')['ConversionRate'].mean()
    st.line_chart(age_conversion)
    
    st.subheader("Campaign Type vs Conversion Rate")
    campaign_conversion = filtered_df.groupby('CampaignType')['LoyaltyPoints'].mean()  # Corrected the grouping syntax
    st.bar_chart(campaign_conversion)

# Area Chart: Repeat Purchases by Campaign Type
st.subheader("Social Shares by Campaign Type")
repeat_purchases_by_campaign = filtered_df.groupby('SocialShares')['PreviousPurchases'].sum()
st.scatter_chart(repeat_purchases_by_campaign)
