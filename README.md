# Rwanda Exports Forecast Dashboard 📊

📌 Problem Statement

Rwanda’s economy relies heavily on international trade, but export performance is influenced by multiple factors such as exchange rates, domestic GDP, and partner countries’ GDP.
The challenge is to build a data-driven forecasting tool that allows stakeholders to:

Anticipate future export trends

Evaluate the impact of macro-economic indicators

Support SMEs, government, and policymakers in making better trade decisions

This project was developed for the Hackathon and provides an **interactive dashboard** to analyze, forecast, and visualize Rwanda’s exports using machine learning models  ectogether with macroecnomic indicators.

---

## 🔹 Data Sources
The dashboard uses multiple datasets including:
- Rwanda’s exports by product categories (HS2 level) from the [Observatory of Economic Complexity (OEC)](https://oec.world/).
- Macroeconomic indicators such as:
  - Rwanda’s GDP and exchange rate (historical + forecasted values).
  - Partner states’ GDP and exchange rate (using IMF forecasts and Prophet models).
- Engineered features such as **weighted GDP**, **weighted exchange rates, moving averages and rolling standard deviations**, and rolling statistical features.

---

## 🔹 What the Dashboard Communicates
The dashboard provides insights into:
- **Historical and forecasted exports** for Rwanda by product and sector or section .
- **Top exports commodities** and their trends over time(from 2018 up to 2030).
- **Partner states analysis**, including total GDP contributions and interactive maps.
- **Recommendations for SMEs, youth, and policymakers** based on forecast results and products that show potential growth.

---

## 🔹 User Interaction
Users can:
- Select **year ranges** via sliders in the sidebar.
- Filter by **section** (product categories) and **products**.
- View **interactive charts** (pie charts, bar charts, line charts, choropleths, bubble maps).
- Explore **tables** of predicted exports with styled formatting and there are downloadabel.
- Navigate across multiple **tabs**, such as:
  1. Home (overview)
  2. Section/Product Analysis
  3. Top Exports Commodities
  4. Recommendations
  5. Partner States Mapping
  6. Technical Details
  7. Row data

---

## 🔹 Technology Stack
- **Python**
- **Streamlit** for dashboard development
- **Plotly Express** for interactive visualizations
- **XGBoost**, **Prophet**, and **Linear Regression** for forecasting
- **Pandas** & **NumPy** for data preprocessing

---
## Purpose of the Dashboard
- Help SMEs and policymakers understand future export trends
- Highlight top export products in different years

🔹 Documentation

This repository includes:

app.py → The main Streamlit dashboard code (runs on any machine).

requirements.txt → Dependencies needed to run the app.

data/ → Preprocessed datasets used in the dashboard.

README.md → Project documentation (this file).


# ⚙️ How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Honore777/Rwanda-export-Forecast-Dashboard.git
   cd Rwanda-export-Forecast-Dashboard
   Right click on app.py then open integrated terminal from there run, streamlit run app.py
   


## Demo video 
### here is the link to the demo video [https://drive.google.com/file/d/1uUOGYX7e6yE0xxMnsBKJajYlXcPeI8-j/view?usp=sharing]


## Streamlit link (deployment link to streamlit app )[https://rwanda-export-forecast-dashboard-miccdu8tgdevspx5hk2gh9.streamlit.app/]


## 👥 Team Information

Team Name: Kepler Data Scientists

Team Members: - Honore HARERIMANA
              -Fabrice Niyigena





