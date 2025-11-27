Rwanda Exports Forecast Dashboard 📊
📌 Problem Statement

Rwanda’s economy relies heavily on international trade, with export performance shaped by key macroeconomic indicators such as exchange rates, domestic GDP, and the GDP of partner countries.

However, Rwanda’s youth, SMEs, and startups still face major challenges when trying to participate in trade or make strategic business decisions. According to national business surveys, about 16% of companies fail due to non-compliance with regulations, often because they lack:

Proper understanding of business, tax, and labor laws

Access to business analysts or data analysts who can guide them

Tools that translate complex economic data into actionable insights

In today’s world — where decisions across finance, trade, and entrepreneurship are data-driven — this lack of analytical support prevents many Rwandan entrepreneurs from identifying high-potential opportunities or avoiding costly business mistakes.

This project addresses these real challenges by providing:

A data-driven export prediction model

A full pipeline that engineers macroeconomic + trade features

An interactive dashboard for SMEs, youth, and policymakers

Agentic AI assistants that help users understand laws and analyze data

Together, these tools democratize access to analytics and compliance information, enabling smarter decisions and reducing startup failure.

🔹 Data Pipeline Overview

The entire data workflow is documented in the Jupyter Notebook
Rwanda Export Prediction Ultimate Model.ipynb, covering:

1. Data Loading

Export data from OEC (HS2 product-level).

Macroeconomic data: Rwanda GDP, exchange rate, partner states’ GDP and exchange rate.

2. Cleaning & Standardization

Removing invalid and missing entries

Normalizing product names, section labels

Merging datasets across multiple years

3. Feature Engineering

Weighted GDP indicators

Weighted exchange rates

Rolling statistical features (moving averages, rolling std)

Growth-based features and trend indicators

4. Model Training

Replaced Prophet with:

➡️ Polynomial Linear Regression (degree 2)

This captures non-linear export behavior while staying interpretable.

5. Final Dataset Export

All processed + predicted data is stored for dashboard consumption.

🔹 Integrated AI Agents

To solve the real challenge of limited access to analysts and legal experts, the dashboard integrates two intelligent assistants:

1. RAG AI Assistant for Rwandan Government Laws 📘

Helps users understand:

Business registration laws

Compliance for SMEs

Tax obligations

Labor regulations

Legal steps to avoid penalties

Uses:

LangChain

ChromaDB vector store

PDF legal materials

Google Gemini AI

OCR (for scanned laws)

This directly tackles the problem that 16% of businesses fail due to legal non-compliance.

2. Pandas AI Agent for Data Analysis 📊

A digital data analyst for users who don’t have one.

It can answer questions like:

“Which exports are growing the fastest?”

“Show me top performing products between 2025–2030.”

“Which partner countries contribute the most GDP share?”

It executes dynamic Pandas code behind the scenes and returns:

Tables

Visualizations

Summaries

Trend statistics

This empowers youth, SMEs, and startups to make data-driven decisions without needing deep technical skills.

🔹 What the Dashboard Communicates

Historical and forecasted exports (2018–2030)

Top commodities and high-growth potential products

Partner states’ GDP and trade influence

AI-powered insights for legal compliance and data exploration

Recommendations for youth, SMEs, and policymakers

🔹 User Interaction Features

Year-range filters

Product and sector selection

Interactive Plotly visualizations

Downloadable styled tables

Multiple tabs for navigation

Built-in AI assistants for laws & data exploration

🔹 Technology Stack

Python

Streamlit

Plotly Express

Polynomial Linear Regression (degree 2)

Pandas & NumPy

LangChain + Chroma + Gemini AI

Tesseract OCR

Pandas AI

🔹 Purpose of the Dashboard

Enable SMEs, youth, and policymakers to understand export dynamics

Reduce startup failure caused by lack of compliance or lack of analytics

Identify high-potential products for investment

Support entrepreneurship through data-driven decision-making

Provide legal and analytical assistance through AI agents

🔹 Documentation

Repository includes:

app.py – Main Streamlit app

requirements.txt – Dependencies

data/ – Final processed datasets

Rwanda Export Prediction Ultimate Model.ipynb – Full modeling pipeline

README.md – Documentation

⚙️ Run Locally
git clone https://github.com/Honore777/Rwanda-export-Forecast-Dashboard.git
cd Rwanda-export-Forecast-Dashboard
pip install -r requirements.txt
streamlit run app.py

🎥 Demo Video

Demo link

🌐 Streamlit Deployment

Live App

👥 Team

Kepler Data Scientists

Honore HARERIMANA

Fabrice Niyigena