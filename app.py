import streamlit as st
import pandas as pd
import numpy as np
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64


st.set_page_config(

    page_title="Rwanda Exports Forecast",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
@st.cache_data
def load_data():
    return pd.read_csv("data/merged_predictions.csv")

df= load_data()

@st.cache_data
def load_partner_states():
    return pd.read_csv("data/data_with_coordinates_and_totalgdp.csv")

data_with_coordinates_and_totalgdp = load_partner_states()


def iso3_from_iso2(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except:
        return None

data_with_coordinates_and_totalgdp["Country_ISO3"] = data_with_coordinates_and_totalgdp["Country_ID"].apply(iso3_from_iso2)


data_with_coordinates_and_totalgdp["TotalGDP"] = pd.to_numeric(data_with_coordinates_and_totalgdp["TotalGDP"], errors="coerce")

st.sidebar.image(
    "assets/NISR.jpg",  # path to your image (local file in your project folder)
    use_container_width=True
)

# Optional: Add a title under the image
st.sidebar.markdown(
    "<h3 style='text-align:center; color:#2563EB;'>Rwanda Exports Forecast Dashboard</h3>",
    unsafe_allow_html=True
)



# --- Sidebar Styling ---
st.markdown(
    """
    <style>
    /* Sidebar container */
    [data-testid="stSidebar"] {
        background-color: lightyellow;  
        padding: 20px 15px;
        border-right: 2px solid #2563EB; /* Blue accent line */
    }

    /* Sidebar labels (sliders text) */
    [data-testid="stSidebar"] label {
        color: #111827;    /* Dark gray text */
        font-size: 16px;
        font-weight: 600;
    }

    /* Slider track */
    [data-testid="stSidebar"] .stSlider > div > div > div {
        background: #2563EB; /* Blue active bar */
    }

    /* Slider thumb (circle) */
    [data-testid="stSidebar"] .stSlider > div > div > div > div {
        background-color: #2563EB;
        border: 2px solid #1E40AF;
    }

    /* Slider number value */
    [data-testid="stSidebar"] .stSlider label div div {
        color: #2563EB !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)




st.markdown(
    """
    <style>
    /* Style the entire info box */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.95);  /* almost solid white */
        border-radius: 8px;
    }

    /* Style text inside the info box */
    .stAlert p,
    .stAlert div,
    .stAlert span {
        color: black !important;    /* force black text */
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True
)





with open("assets/Rwanda tea plantation.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()


st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)





st.markdown("""
<style>
/* Whole tab bar background */
.stTabs [role="tablist"] {
    background-color: #f5f5f5;
    padding: 5px;
    border-radius: 8px;
}

/* 1st tab: blue */
.stTabs [role="tablist"] button:nth-of-type(1) {
    background-color: #009EE0 !important; /* Rwanda blue */
    color: white !important;
    border-radius: 6px;
}

/* 2nd tab: yellow */
.stTabs [role="tablist"] button:nth-of-type(2) {
    background-color: #FCD116 !important; /* Rwanda yellow */
    color: #111 !important;
    border-radius: 6px;
}

/* 3rd tab: green */
.stTabs [role="tablist"] button:nth-of-type(3) {
    background-color: #007A33 !important; /* Rwanda green */
    color: white !important;
    border-radius: 6px;
}

/* 4th tab: light blue (variation) */
.stTabs [role="tablist"] button:nth-of-type(4) {
    background-color: #66CFFF !important;
    color: #111 !important;
    border-radius: 6px;
}

/* 5th tab: light yellow (variation) */
.stTabs [role="tablist"] button:nth-of-type(5) {
    background-color: #FFE65B !important;
    color: #111 !important;
    border-radius: 6px;
}

/* 6th tab: light green (variation) */
.stTabs [role="tablist"] button:nth-of-type(6) {
    background-color: #5AD48C !important;
    color: #111 !important;
    border-radius: 6px;
}
            
.stTabs [role="tablist"] button:nth-of-type(7) {
    background-color: #66CFFF !important;
    color: #111 !important;
    border-radius: 6px;
}           

/* optional: make active tab a bit darker */
.stTabs [role="tablist"] button[aria-selected="true"] {
    filter: brightness(90%);
}
</style>
""", unsafe_allow_html=True)




tabs= st.tabs([

    "Home / Overview",
    "Export Forecasts by Product",
    "Economic Indicators",
    "Top Export Opportunities & Recommendations",
    "Partner States GDP Map",
    "Technical Explanation",
    "Raw Data & Download"
])








with tabs[0]:
    
    st.markdown("""
<div style="
    background-color:#009EE0;   /* Rwanda blue */
    color:white;
    padding:25px;
    border-radius:12px;
    display:flex;
    align-items:center;
    gap:15px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
    margin-bottom:20px;
">
    <img src="https://upload.wikimedia.org/wikipedia/commons/1/17/Flag_of_Rwanda.svg" width="80" style="border-radius:5px;">
    <div>
        <h1 style="margin:0;">Rwanda Exports Forecast Dashboard</h1>
        <p style="margin:5px 0 0; font-size:18px; color:#F3F4F6;">
            See the total predicted exports per year and the top 10 export commoditites from 2018 up to 2030.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    # Intro 
    st.markdown("""
    <div style="
        background-color:#F3F4F6;  /* light gray */
        color:#111827;               /* dark text */
        padding:15px;
        border-left: 5px solid #2563EB;  /* blue accent */
        border-radius:8px;
        margin-bottom:15px;
    ">
        <p style="font-size:16px; line-height:1.5;">
        Welcome to the Rwanda Export Forecast Dashboard. This tool predicts future export trends 
        to help SMEs, youth and the government make informed decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")  # horizontal line

    # Sections list
    st.markdown("""
    <div style="
        padding:12px; 
        background-color:#DBEAFE; /* light blue background */
        border-radius:10px;
        color:#1E3A8A;             /* dark blue text */
    ">
    <h2 style="margin-bottom:10px;">Sections of the Dashboard:</h2>
    <ul style="font-size:16px; line-height:1.6;">
        <li><b>Home / Overview:</b> Summary of total predicted exports and top products.</li>
        <li><b>Export Forecasts by Product:</b> Drill down by sector/product to see trends.</li>
        <li><b>Economic Indicators:</b> See GDP, exchange rates, and weighted GDP values of partner states.</li>
        <li><b>Top Export Opportunities & Recommendations:</b> Shows the top 10 future exports and suggestions for SMEs/Government.</li>
        <li><b>Partner States GDP Map:</b> Shows our partner states we export products to in terms of their total GDP from 2018 up to 2030 (map format).</li>
        <li><b>Technical Explanation:</b> Explains model, metrics, and feature engineering.</li>
        <li><b>Raw Data & Download:</b> View and download the underlying dataset.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    total_exports= df.groupby("Year")['Predicted_Exports'].sum()
    # Convert series to dataframe
    total_exports_df = total_exports.reset_index()
    total_exports_df.columns = ['Year', 'Predicted_Exports']



    
    # --- Defaults ---
    if 'current_year' not in st.session_state:
        st.session_state['current_year'] = 2025
    if 'projection_year' not in st.session_state:
        st.session_state['projection_year'] = 2026

    # --- Sliders (always displayed) ---
    st.session_state['current_year'] = st.sidebar.slider(
        "Select Current Year",
        int(df['Year'].min()),
        int(df['Year'].max()),
        value=st.session_state['current_year']  # default value
    )

    st.session_state['projection_year'] = st.sidebar.slider(
        "Select Projection Year",
        int(df['Year'].min()),
        int(df['Year'].max()),
        value=2026
    )
    st.info("Use the sidebar to compare exports for different years and compute growth")
    #  Compute metrics
    total_exports_for_current_year = df[df['Year']==st.session_state['current_year']]['Predicted_Exports'].sum()
    total_exports_for_projection_year = df[df['Year']==st.session_state['projection_year']]['Predicted_Exports'].sum()

    growth_between_years = (total_exports_for_projection_year - total_exports_for_current_year) / total_exports_for_current_year * 100



    col1, col2, col3 = st.columns(3)

    

    card_style_blue = """
    <div style="
        background-color:#009EE0;  /* Rwanda blue */
        color:white;
        padding:25px;
        border-radius:12px;
        min-height:150px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    <p>{delta}</p>
    </div>
    """
    card_style_yellow = """
    <div style="
        background-color:#FCD116;  /* Rwanda yellow */
        color:#111827;
        padding:25px;
        border-radius:12px;
        min-height:150px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    <p>{delta}</p>
    </div>
    """
    card_style_green = """
    <div style="
        background-color:#007A33;  /* Rwanda green */
        color:white;
        padding:25px;
        border-radius:12px;
        min-height:150px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    <p>{delta}</p>
    </div>
    """


    # Card 1
    with col1:
        st.markdown(card_style_blue.format(
            label=f"Exports {st.session_state['current_year']}",
            value=f"${total_exports_for_current_year:,.0f}",
            delta=f"{growth_between_years:+.2f}%"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(card_style_yellow.format(
            label=f"Predicted Exports {st.session_state['projection_year']}",
            value=f"${total_exports_for_projection_year:,.0f}",
            delta=""
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(card_style_green.format(
            label=f"Growth({st.session_state['current_year']} _ {st.session_state['projection_year']}) (%)",
            value=f"{growth_between_years:,.2f}%",
            delta=""
        ), unsafe_allow_html=True)

        st.markdown("---")

    
    st.markdown("""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
        Total Predicted Exports(USD) over Years
    </h2>
""", unsafe_allow_html=True)

    fig = px.line(
        total_exports_df,
        x='Year',
        y='Predicted_Exports',
        markers=True,
        labels={"Predicted_Exports": "Exports (USD)", "Year": "Year"},
        line_shape="linear",
        text=total_exports_df["Predicted_Exports"]  # show values on points
    )

    # Customize line, markers, and point text
    fig.update_traces(
        line=dict(color="#009EE0", width=3),  # Rwanda blue line
        marker=dict(size=10, color="#007A33", line=dict(width=2, color="#00491C")),  # green points with border
        texttemplate='%{text:,.0f}',  # display values
        textposition='top center',
        hovertemplate="<b>Year:</b> %{x}<br><b>Exports:</b> %{y:,.0f}<extra></extra>"
    )

    # Layout with visible axes on gray background
    fig.update_layout(
        yaxis=dict(
            tickformat=',', 
            title=dict(text="Exports (USD)", font=dict(color="#111827", size=14)),
            tickfont=dict(color="#111827", size=12),
            gridcolor="#E5E7EB",  
            zerolinecolor="#111827"
        ),
        xaxis=dict(
            title=dict(text="Year", font=dict(color="#111827", size=14)),
            tickfont=dict(color="#111827", size=12),
            gridcolor="#E5E7EB",
            zerolinecolor="#111827",
            dtick=1
        ),
        plot_bgcolor="#F9FAFB",  # chart background
        paper_bgcolor="#F3F4F6", # dashboard background
        font=dict(color="#111827"),
        margin=dict(l=60, r=30, t=30, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)






    if 'year' not in st.session_state:
            st.session_state['year'] = 2025

    st.markdown("---")
    st.info("Select a year to view the top 5 export products for that year")

    st.session_state['year']= st.selectbox(
            "SELECT YEAR",
            options=df['Year'].unique(), index=list(sorted(df["Year"].unique())).index(st.session_state.year)
            
        )




    # Top 10 products for selected year
    top_products = (
        df[df['Year']==st.session_state['year']]
        .sort_values(by='Predicted_Exports', ascending=False)
        .head(10)    
    )

    
    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
       Top 10 Exports commodities in {st.session_state.year}
    </h2>
""", unsafe_allow_html=True)
    

   



    fig = px.bar(
        top_products,
        x="HS2",
        y="Predicted_Exports",
        text="Predicted_Exports"
    )

    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="white",   
        paper_bgcolor="#F9FAFB", 
        font=dict(color="#111827"),  
        
        yaxis=dict(
            tickformat=',',
            title="Predicted Exports (USD)",
            title_font=dict(color="black", size=14),   # Y-axis title darker
            tickfont=dict(color="black", size=12)      # Y-axis ticks darker
        ),
        xaxis=dict(
            title="Product (HS2)",
            title_font=dict(color="black", size=14),   # X-axis title darker
            tickfont=dict(color="black", size=12)      # X-axis ticks darker
        )
    )

    st.plotly_chart(fig, use_container_width=True)



        # Style the dataframe
    st.dataframe(
            top_products[['Section', 'HS2','Year','Share (%)','TotalExportsYear','Predicted_Exports']]
            .style.set_properties(
                **{
                    'background-color': '#F9FAFB',  # very light gray
                    'color': '#111827',              # dark text
                    'border-color': '#E5E7EB',
                    'border-width':'1px',
                    'text-align': 'center'
                }
            )
        )

        # Bar chart with Rwanda colors
    


   

        
    


     










    

    
        

    
with tabs[1]:
    if 'section' not in st.session_state:
        st.session_state['section'] = "Mineral Products"
    if 'hs2' not in st.session_state:
        st.session_state['hs2'] = "Ores, slag and ash"

    st.markdown("""
    <h1 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
        Export Forecasts by Product
    </h1>
""", unsafe_allow_html=True)

    section = st.selectbox("SELECT SECTION (FILTER)", options=df['Section'].unique())
    st.session_state['section'] = section
    df_section = df[df['Section'] == section]

    product = st.selectbox("SELECT PRODUCT(HS2)", df_section["HS2"].unique())
    st.session_state['hs2'] = product
    product_df = df_section[df_section["HS2"] == product].sort_values("Year")
    
    current_year = st.session_state['current_year']
    projection_year = st.session_state['projection_year']

    product_df_n = product_df[product_df['Year'] == current_year]['Predicted_Exports'].sum()
    product_df_p = product_df[product_df['Year'] == projection_year]['Predicted_Exports'].sum()
    perc_growth = (product_df_p - product_df_n) / product_df_n * 100

    st.info('Use the sidebar to compare the selected export commodity (HS2) in different years.')

    # --- Metrics styled ---
    col1, col2, col3 = st.columns(3)

    card_blue = """
    <div style="
        background-color:#009EE0;
        color:white;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow:2px 2px 12px rgba(0,0,0,0.2);
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    <p>{delta}</p>
    </div>
    """
    card_yellow = """
    <div style="
        background-color:#FCD116;
        color:#111827;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow:2px 2px 12px rgba(0,0,0,0.2);
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    <p>{delta}</p>
    </div>
    """
    card_green = """
    <div style="
        background-color:#007A33;
        color:white;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow:2px 2px 12px rgba(0,0,0,0.2);
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    <p>{delta}</p>
    </div>
    """

    col1.markdown(card_blue.format(
        label=f"{product} exports ({current_year})",
        value=f"${product_df_n:,.0f}",
        delta=""
    ), unsafe_allow_html=True)

    col2.markdown(card_yellow.format(
        label=f"{product} exports ({projection_year})",
        value=f"${product_df_p:,.0f}",
        delta=""
    ), unsafe_allow_html=True)

    col3.markdown(card_green.format(
        label=f"Growth ({current_year} _ {projection_year}) (%)",
        value=f"{perc_growth:,.2f}%",
        delta=""
    ), unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
       Historical and Predicted Exports: {product}
    </h2>
""", unsafe_allow_html=True)


    # Line chart
    # --- Line chart ---
    fig = px.line(
    product_df,
    x="Year",
    y="Predicted_Exports",
    markers=True,
    labels={"Predicted_Exports": "Exports (USD)"}
)

    fig.update_traces(
    line=dict(color="#009EE0", width=3),
    marker=dict(size=8, color="#007A33", line=dict(width=2, color="#00491C")),
    hovertemplate="<b>Year:</b> %{x}<br><b>Exports:</b> %{y:,.0f}<extra></extra>"
)

    fig.update_layout(
    plot_bgcolor="white",      # chart background
    paper_bgcolor="#F9FAFB",   # around chart
    font=dict(color="#111827"),
    yaxis=dict(
        tickformat=',',
        title="Exports (USD)",
        title_font=dict(color="black", size=14),
        tickfont=dict(color="black", size=12),
        showgrid=False,        # remove gridlines
        zeroline=False
    ),
    xaxis=dict(
        dtick=1,
        title="Year",
        title_font=dict(color="black", size=14),
        tickfont=dict(color="black", size=12),
        showgrid=False,        # remove gridlines
        zeroline=False
    ),
    margin=dict(l=60, r=30, t=30, b=50)
)

    st.plotly_chart(fig, use_container_width=True)


    st.info('Use the sidebar to see product share in the selected year.')

    # --- Pie chart ---
    
    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
       Share of {product} in {section} ({current_year}
    </h2>
""", unsafe_allow_html=True)

    df_year_section = df_section[df_section['Year'] == current_year]
    df_year_section = df_year_section.assign(
        Share_Percent = df_year_section['Predicted_Exports'] / df_year_section['Predicted_Exports'].sum() * 100
    )

    fig_pie = px.pie(
    df_year_section,
    names="HS2",
    values="Predicted_Exports",
    title="Products' share in section exports",
    color_discrete_sequence=["#009EE0", "#FCD116", "#007A33", "#F9A11B", "#00491C"]
)

    fig_pie.update_traces(
        textinfo='percent',  # only percent inside slices
        textfont=dict(color="black", size=12),
        hovertemplate="<b>%{label}:</b> %{value:,.0f}<extra></extra>",
        showlegend=True
    )

    fig_pie.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#F9FAFB",
        font=dict(color="#111827"),
        legend=dict(
            title="Products",
            font=dict(color="black", size=12)
        ),
        title=dict(
            font=dict(color="black", size=16)
        ),
        margin=dict(l=30, r=30, t=50, b=30)
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # --- Stacked bar chart ---
    
    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
       Top 5 Products in {section} by Year
    </h2>
""", unsafe_allow_html=True)

    top5_products = df_section.groupby("HS2")['Predicted_Exports'].sum().sort_values(ascending=False).head(5).index
    df_top5 = df_section[df_section['HS2'].isin(top5_products)]

    fig_bar = px.bar(
    df_top5,
    x="Year",
    y="Predicted_Exports",
    color="HS2",
    barmode="stack",
    labels={"Predicted_Exports": "Exports (USD)", "HS2": "Product"},
    color_discrete_sequence=["#009EE0", "#FCD116", "#007A33", "#F9A11B", "#00491C"],
    text='Predicted_Exports'
)

    fig_bar.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='inside'
    )

    fig_bar.update_layout(
        plot_bgcolor="white",     # chart area
        paper_bgcolor="#F9FAFB",  # around chart
        font=dict(color="black"),
        yaxis=dict(
    tickformat=',',
    title=dict(text="Exports (USD)", font=dict(color="black", size=14)),
    tickfont=dict(color="black", size=12, family="Arial Black"),  # makes labels darker/bolder
    
),
        xaxis=dict(
            dtick=1,
            title=dict(text="Year", font=dict(color="black", size=14)),
            tickfont=dict(color="black", size=12, family="Arial Black"),  # bold & dark

        ),

                legend=dict(
                    title="Products",
                    font=dict(color="black", size=1)
                ),
                margin=dict(l=40, r=30, t=50, b=50)
            )
    st.plotly_chart(fig_bar, use_container_width=True)


    # --- Predicted table ---
    

    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
      Predicted Exports Table
    </h2>
""", unsafe_allow_html=True)

    
    future_predictions = product_df[product_df['Data_Type'] == 'Forecast']
    st.markdown(
    """
    <style>
    [data-testid="stDataFrame"] div[data-testid="stStyledTable"] {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    
    st.dataframe(
           future_predictions[["Year", "HS2", "Predicted_Exports", "Share (%)", "TotalExportsYear"]]
           
            .style.set_properties(
                **{
                    'background-color': '#F9FAFB',  # very light gray
                    'color': '#111827',              # dark text
                    'border-color': '#E5E7EB',
                    'border-width':'1px',
                    'text-align': 'center'
                }
            )
        )






with tabs[2]:
    
    st.markdown(f"""
    <h1 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:52px;             
    ">
     Economic Indicators
    </h1>
""", unsafe_allow_html=True)


    year= st.session_state['current_year']
    df_year = df[df['Year'] == year]

    avg_gdp = df_year['GDP'].mean()
    avg_fx = df_year['Predicted_Exchange_Rate'].values[0]
    weighted_gdp_fx = (df_year['GDP'] * df_year['Predicted_Exchange_Rate']).mean()
    partner_weighted_gdp= df_year['WeightedGDP'].mean()
    partner_weighted_exchange_rate= df_year['WeightedFX'].mean()

    card_style_blue = """
    <div style="
        background-color:#009EE0;
        color:white;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        min-height:140px;
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    </div>
    """

    card_style_yellow = """
    <div style="
        background-color:#FCD116;
        color:#111827;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        min-height:140px;
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    </div>
    """

    card_style_green = """
    <div style="
        background-color:#007A33;
        color:white;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        min-height:140px;
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    </div>
    """
    col4,col5,col6 = st.columns(3)

    st.info('Use the sidebar to select year to compare these economic indicators in different years.')
    # Display cards
    with col4:
        st.markdown(card_style_blue.format(
            label=f"Average GDP of Rwanda {year}",
            value=f"${avg_gdp:,.0f}"
        ), unsafe_allow_html=True)
    
    with col5:
        st.markdown(card_style_yellow.format(
            label=f" Exchange Rate of Rwanda in {year}",
            value=f"{avg_fx:,.2f} RWF/USD"
        ), unsafe_allow_html=True)

    with col6:
        st.markdown(card_style_green.format(
            label=f"Average Weighted GDP of partner states in {year}",
            value=f"${partner_weighted_gdp:,.0f}"
        ), unsafe_allow_html=True)

   

# Example groupings
    gdp_over_years = df.groupby("Year")["GDP"].mean().reset_index()
    fx_over_years = df.groupby("Year")["Predicted_Exchange_Rate"].mean().reset_index()
    weighted_fx_gdp = df.groupby("Year")["FX_x_WeightedGDP"].mean().reset_index()
    weight_partner_weighted_gdp= df.groupby("Year")["WeightedGDP"].mean().reset_index()


# --- Rwanda GDP Over Years ---
    st.markdown(f"""
        <h1 style="
            text-align:center;
            background-color:#2563EB;   
            color:white;                
            padding:15px;               
            margin:20px 0;          
            border-radius:8px;          
            font-size:32px;             
        ">
        Rwanda GDP Over Years
        </h1>
    """, unsafe_allow_html=True)

    fig_gdp = px.line(
        gdp_over_years,
        x="Year",
        y="GDP",
        markers=True,
        labels={"GDP": "GDP (USD)"}
    )

    fig_gdp.update_traces(
        line=dict(color="#009EE0", width=3),
        marker=dict(size=8, color="#007A33", line=dict(width=2, color="#00491C")),
        hovertemplate="<b>Year:</b> %{x}<br><b>GDP:</b> %{y:,.0f}<extra></extra>"
    )

    fig_gdp.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#F9FAFB",
        font=dict(color="#111827"),
        yaxis=dict(
            tickformat=',',
            title="GDP (USD)",
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black", size=12),
            showgrid=False,
            zeroline=False
        ),
        xaxis=dict(
            dtick=1,
            title="Year",
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black", size=12),
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=60, r=30, t=30, b=50)
    )
    st.plotly_chart(fig_gdp, use_container_width=True)


    # --- Rwanda Exchange Rate Over Years ---
    st.markdown(f"""
        <h1 style="
            text-align:center;
            background-color:#2563EB;   
            color:white;                
            padding:15px;               
            margin:20px 0;          
            border-radius:8px;          
            font-size:32px;             
        ">
        Rwanda Exchange Rate Over Years
        </h1>
    """, unsafe_allow_html=True)

    fig_fx = px.line(
        fx_over_years,
        x="Year",
        y="Predicted_Exchange_Rate",
        markers=True,
        labels={"Predicted_Exchange_Rate": "Exchange Rate (RWF/USD)"}
    )

    fig_fx.update_traces(
        line=dict(color="#009EE0", width=3),
        marker=dict(size=8, color="#F97316", line=dict(width=2, color="#7C2D12")),
        hovertemplate="<b>Year:</b> %{x}<br><b>Exchange Rate:</b> %{y:,.2f}<extra></extra>"
    )

    fig_fx.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#F9FAFB",
        font=dict(color="#111827"),
        yaxis=dict(
            tickformat=',',
            title="Exchange Rate (RWF/USD)",
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black", size=12),
            showgrid=False,
            zeroline=False
        ),
        xaxis=dict(
            dtick=1,
            title="Year",
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black", size=12),
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=60, r=30, t=30, b=50)
    )
    st.plotly_chart(fig_fx, use_container_width=True)


    # --- Weighted GDP of Partner States ---
    st.markdown(f"""
        <h1 style="
            text-align:center;
            background-color:#2563EB;   
            color:white;                
            padding:15px;               
            margin:20px 0;          
            border-radius:8px;          
            font-size:32px;             
        ">
        Weighted GDP of partners states
        </h1>
    """, unsafe_allow_html=True)

    fig_weighted = px.line(
        weight_partner_weighted_gdp,
        x="Year",
        y="WeightedGDP",
        markers=True,
        labels={"WeightedGDP": "Weighted GDP * FX"}
    )

    fig_weighted.update_traces(
        line=dict(color="#009EE0", width=3),
        marker=dict(size=8, color="#10B981", line=dict(width=2, color="#064E3B")),
        hovertemplate="<b>Year:</b> %{x}<br><b>Value:</b> %{y:,.0f}<extra></extra>"
    )

    fig_weighted.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#F9FAFB",
        font=dict(color="#111827"),
        yaxis=dict(
            tickformat=',',
            title="Weighted GDP * FX",
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black", size=12),
            showgrid=False,
            zeroline=False
        ),
        xaxis=dict(
            dtick=1,
            title="Year",
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black", size=12),
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=60, r=30, t=30, b=50)
    )
    st.plotly_chart(fig_weighted, use_container_width=True)


with tabs[3]:
    
    st.markdown(f"""
    <h1 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:52px;             
    ">
    Top Export Opportunities & Recommendations
    </h1>
""", unsafe_allow_html=True)


    year = st.session_state['current_year']
    df_year = df[df['Year'] == year]

   
    top10 = df_year.sort_values(by="Predicted_Exports", ascending=False).head(10)

    # Metrics
    total_exports = df_year['Predicted_Exports'].sum()
    top_commodity = top10.iloc[0]
    top_commodity1=top_commodity['HS2']
    top_commodity_exports = top_commodity['Predicted_Exports']

    # Compare top commodity to previous year
    prev_year = year - 1
    prev_year_exports = df[(df['Year'] == prev_year) & (df['HS2'] == top_commodity['HS2'])]['Predicted_Exports'].sum()
    growth_top_commodity = ((top_commodity_exports - prev_year_exports) / prev_year_exports * 100) 

    # Cards
    st.info('To compare top export commodities in different years from 2018 up to 2030 use the sidebar slider to select year')
    col1, col2, col3 = st.columns(3)

    card_style_blue = """
    <div style="
        background-color:#009EE0;
        color:white;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        min-height:140px;
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    </div>
    """
    card_style_yellow = """
    <div style="
        background-color:#FCD116;
        color:#111827;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        min-height:140px;
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    </div>
    """
    card_style_green = """
    <div style="
        background-color:#007A33;
        color:white;
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        min-height:140px;
    ">
    <h3>{label}</h3>
    <h1>{value}</h1>
    </div>
    """
    
    with col1:
        st.markdown(card_style_blue.format(
            label=f"Total Exports {year}",
            value=f"${total_exports:,.0f}"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(card_style_yellow.format(
            label=f"Top Commodity in {year}: {top_commodity['HS2']}",
            value=f"${top_commodity_exports:,.0f}"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(card_style_green.format(
            label=f"Growth of {top_commodity1} relative to {prev_year} ",
            value=f"{growth_top_commodity:,.2f}%"
        ), unsafe_allow_html=True)

    # Chart: Top 10 predicted exports in selected year

    st.markdown(f"""
    <h1 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
    Top 10  Exports commodities in {year}
    </h1>
""", unsafe_allow_html=True)

    fig_bar = px.bar(
        top10,
        x="HS2",
        y="Predicted_Exports",
        color="Section",
        labels={"Predicted_Exports":"Exports (USD)", "HS2":"Product"},
        text="Predicted_Exports"
    )
    fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig_bar.update_layout(
        yaxis=dict(tickformat=','),
        xaxis=dict(tickangle=-45)
    )
    st.plotly_chart(fig_bar, use_container_width=True)



    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
    Top  Exports Commodities in {  st.session_state['current_year'] }
    </h2>
""", unsafe_allow_html=True)


    st.dataframe(top10[["HS2", "Section",'Year', "Predicted_Exports", "Share (%)"]])

    st.subheader("Recommendations for SMEs and Government")

    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
    Recommendations for SMEs and Government 
    </h2>
""", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background-color:#F3F4F6;
        color:#111827;
        padding:15px;
        border-left: 5px solid #2563EB;
        border-radius:8px;
        line-height:1.6;
    ">
    <b>For Government & Policy Makers:</b><br>
    – Prioritise high-growth sectors such as Precious Metals, Mineral Products, Coffee and Tea, and ICT services.  
    – Develop export-friendly policies (tax incentives, infrastructure, certification support) to help SMEs and youth-owned enterprises compete internationally.  
    – Create incubation programmes and targeted financing for youth-led ventures in these sectors.  

    <br><b>For SMEs:</b><br>
    – Use this dashboard to identify products and sections with rising export potential.  
    – Diversify your product portfolio in line with sectors forecast to grow.  
    – Partner with other firms to achieve scale and meet export standards.  

    <br><b>For Youth & Aspiring Entrepreneurs:</b><br>
    – Explore the <i>Section</i> filter to discover areas you’re passionate about.  
    – Look at the forecast charts to see which products are expected to grow most in future years.  
    – Use this insight to design your business plan — focus on a product with strong future export potential.  
    – Seek training and mentorship from government programmes aligned with these sectors.  

    <br>
    <b>Tip:</b> This dashboard is an interactive guide — slide through the years on the sidebar, check the sections, and use the forecasts to inform your strategic decisions.
    </div>
    """, unsafe_allow_html=True)


with tabs[4]:
    st.markdown("""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:28px;             
    ">
       Partner States Map (GDP 2028-2030)
    </h2>
    """, unsafe_allow_html=True)

    st.info('This is map of partner countries, the size of the bubble depends on the size of  the total GDP of that country from 2018 up to 2030, You can hover over the bubbles to see the country, their GDP and population')

    # Bubble Map
    fig_bubble = px.scatter_geo(
    data_with_coordinates_and_totalgdp,
    lat='latitude',
    lon='longitude',
    size='TotalGDP',
    color='TotalGDP',
    color_continuous_scale=["#007A33", "#FCD116", "#009EE0"],  # Rwanda flag colors
    projection='natural earth',
    hover_name='Country',  # only show name on hover
    hover_data={'TotalGDP': ':,', 'GDP': ':,', 'population': True}
)

# Remove text labels on bubbles
    fig_bubble.update_traces(text=None)

    fig_bubble.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
        plot_bgcolor='#F9FAFB',
        paper_bgcolor='#F3F4F6',
        font=dict(color="#111827"),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)



    fig_choropleth = px.choropleth(
    data_with_coordinates_and_totalgdp,
    locations="Country_ISO3",
    color="TotalGDP",
    hover_name="Country",
    hover_data={"GDP":":,", "population":True},
    color_continuous_scale=[
        "#006837",  # dark green
        "#FCD116",  # yellow
        "#F97316",  # orange
        "#DC2626",  # red
        "#7E22CE",  # purple
        "#2563EB"   # blue
    ],
    projection="natural earth"
)

    fig_choropleth.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
        title=dict(text="Partner States Total GDP (2028–2030)", x=0.5, xanchor='center'),
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color="#111827"),
        coloraxis_colorbar=dict(
            title="Total GDP",
            tickformat=","
        )
    )

    st.plotly_chart(fig_choropleth, use_container_width=True)





with tabs[5]:  # Technical / Methodology Tab

    st.markdown(f"""
    <h1 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:52px;             
    ">
    Technical Approach & Methodology 
    </h1>
""", unsafe_allow_html=True)





    st.markdown("""
    <div style="
        background-color:#F3F4F6;
        color:#111827;
        padding:20px;
        border-left:5px solid #2563EB;
        border-radius:10px;
        font-size:16px;
        line-height:1.6;
    ">

    <h2 style="margin-top:0;">1. Hybrid Modelling Strategy</h2>
    <ul>
      <li><b>Main model:</b> <b>XGBoost</b> to predict total exports. It captures non-linear relationships between macroeconomic indicators and exports.</li>
      <li><b>Complementary models:</b>
        <ul>
          <li>Polynomial Linear Regression (degree 2): predicts Rwanda’s exchange rate trends.</li>
          <li>Prophet: forecasts partner states’ exchange rates.</li>
          <li>IMF GDP forecasts integrated for partner GDP levels.</li>
        </ul>
      </li>
    </ul>

    <h2>2. Why XGBoost for Future Forecasting</h2>
    <p>Exports depend on multiple exogenous variables (GDP growth, exchange rates, partner demand) which do not follow purely linear trends. Feature-engineered ensemble models like XGBoost are more appropriate than a single classical time-series approach.</p>

    <h2>3. Feature Engineering</h2>
    <ul>
      <li><b>Rolling windows:</b> moving averages and rolling standard deviations capture short-term volatility and long-term trends.</li>
      <li><b>Target lags:</b> past values of exports as predictors allow the model to learn temporal patterns.</li>
      <li><b>Weighted GDP & Exchange Rates:</b> partner states’ GDP and exchange rates weighted by trade share reflect the economic health of destination markets.</li>
      <li><b>Rwanda’s indicators:</b> GDP, GDP growth, exchange rate, and exchange-rate growth included as features.</li>
    </ul>

    <h2>4. Forecasting Pipeline</h2>
    <ol>
      <li>Forecast partner-state GDP and exchange rates (Prophet + IMF).</li>
      <li>Forecast Rwanda’s exchange rate (Polynomial Regression).</li>
      <li>Assemble all features (current + forecasted) into XGBoost.</li>
      <li>Generate export projections for future years.</li>
      <li>We used a recursive apprach with walk forward retraining so that our model can make suitable splits and prevent it from accumulating errors.</li>
    </ol>

    <h2>5. Data Sources</h2>
    <ul>
      <li><b>Rwanda NISR</b> and <b>Rwanda Revenue Authority</b>: base trade data.</li>
      <li><b>OEC (Observatory of Economic Complexity):</b> used to validate HS2-level exports and partner data.</li>
      <li><b>IMF WEO:</b> GDP forecasts.</li>
      <li>Exchange-rate feeds for partner currencies.</li>
    </ul>

    <h2>6. Limitations</h2>
    <ul>
      <li><b>Data scarcity:</b> lack of consistent partner-level forecasts required aggregation (weighted GDP/exchange rate).</li>
      <li><b>Forecast uncertainty:</b> macroeconomic projections introduce uncertainty into export forecasts.</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("")




    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
    Sample Feature Engineering Code
    </h2>
""", unsafe_allow_html=True)







    st.code("""
# Creating lag, moving average and growth features
df_all['Revenue_Lag1'] = df_all.groupby('HS2')['Predicted_Exports'].shift(1)

df_all['Revenue_MA3'] = (
    df_all.groupby('HS2')['Predicted_Exports']
          .transform(lambda x: x.rolling(3, min_periods=1).mean())
)

df_all['Revenue_Growth'] = (
    df_all.groupby('HS2')['Predicted_Exports'].pct_change()
)
    """)


    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
    Model training Codes
    </h2>
""", unsafe_allow_html=True)



    st.code("""
    mport pandas as pd
    from xgboost import XGBRegressor

    df_all["Predicted_Exports"] = df_all["Exports (USD)"].copy()

    forecast_years = sorted(df_all[df_all["Data_Type"]=="Forecast"]["Year"].unique())

    # Features list for XGBoost
    features = [
        # Revenue features
        "Revenue_Lag1", "Revenue_Lag2", "Revenue_Lag3",
        "Revenue_MA3", "Revenue_MA5", "Revenue_STD3", "Revenue_Growth",

        # Exchange rate features
        "FX_Lag1", "FX_Lag2", "FX_MA3", "FX_Growth", "FX_x_WeightedGDP",
        "GDP_Lag1", "GDP_Lag2", "GDP_MA3", "GDP_Growth",


        "WeightedGDP", "WeightedFX"
    ]
    target = "Exports (USD)"

    for year in forecast_years:
        print(f"Predicting year {year}...")

        # Sort for proper lag/rolling calculations
        df_all = df_all.sort_values(by=["HS2", "Year"]).reset_index(drop=True)

        
        df_all["Revenue_Lag1"] = df_all.groupby("HS2")["Predicted_Exports"].shift(1)
        df_all["Revenue_Lag2"] = df_all.groupby("HS2")["Predicted_Exports"].shift(2)
        df_all["Revenue_Lag3"] = df_all.groupby("HS2")["Predicted_Exports"].shift(3)
        df_all["Revenue_MA3"] = df_all.groupby("HS2")["Predicted_Exports"].transform(lambda x: x.rolling(3, min_periods=1).mean())
        df_all["Revenue_MA5"] = df_all.groupby("HS2")["Predicted_Exports"].transform(lambda x: x.rolling(5, min_periods=1).mean())
        df_all["Revenue_STD3"] = df_all.groupby("HS2")["Predicted_Exports"].transform(lambda x: x.rolling(3, min_periods=1).std())
        df_all["Revenue_Growth"] = df_all.groupby("HS2")["Predicted_Exports"].pct_change()

    
        df_all["FX_Lag1"] = df_all.groupby("HS2")["Predicted_Exchange_Rate"].shift(1)
        df_all["FX_Lag2"] = df_all.groupby("HS2")["Predicted_Exchange_Rate"].shift(2)
        df_all["FX_MA3"] = df_all.groupby("HS2")["Predicted_Exchange_Rate"].transform(lambda x: x.rolling(3, min_periods=1).mean())
        df_all["FX_Growth"] = df_all.groupby("HS2")["Predicted_Exchange_Rate"].pct_change()
        df_all["FX_x_WeightedGDP"] = df_all["Predicted_Exchange_Rate"] * df_all["WeightedGDP"]

        df_all["GDP_Lag1"] = df_all.groupby("HS2")["GDP"].shift(1)
        df_all["GDP_Lag2"] = df_all.groupby("HS2")["GDP"].shift(2)
        df_all["GDP_MA3"] = df_all.groupby("HS2")["GDP"].transform(lambda x: x.rolling(3, min_periods=1).mean())
        df_all["GDP_Growth"] = df_all.groupby("HS2")["GDP"].pct_change()

        train_df = df_all[df_all["Year"] < year].copy()
        train_df = train_df[train_df["Predicted_Exports"].notna()]
        X_train = train_df[features]
        y_train = train_df["Predicted_Exports"]

        
        predict_df = df_all[df_all["Year"] == year].copy()
        X_pred = predict_df[features]

        
        model = XGBRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            max_depth=10,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=5,
            reg_lambda=1,
            reg_alpha=0.1,
            gamma=0.1,
            tree_method="hist",
            random_state=42
        )
        model.fit(X_train, y_train)

        
        df_all.loc[df_all["Year"] == year, "Predicted_Exports"] = model.predict(X_pred)

        total_exports = df_all[df_all["Year"] == year]["Predicted_Exports"].sum()
        df_all.loc[df_all["Year"] == year, "TotalExportsYear"] = total_exports
        df_all.loc[df_all["Year"] == year, "Share (%)"] = df_all[df_all["Year"] == year]["Predicted_Exports"] / total_exports

        print(f"Year {year} predicted successfully.")

        """)

    st.markdown(f"""
    <h2 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:32px;             
    ">
    Model Accuracy Metrics
    </h2>
""", unsafe_allow_html=True)



    st.markdown("""
                <div style="
        background-color:#F3F4F6;
        color:#111827;
        padding:20px;
        border-left:5px solid #2563EB;
        border-radius:10px;
        font-size:16px;
        line-height:1.6;
    ">
        <li>R² Score:<strong> 0.86</strong></li>
        <li>MAE: <strong> 4,408,190 USD </strong></li> 
        <li>RMSE:<strong>30,849,170 USD  </strong></li>
        </div>
    """,unsafe_allow_html=True)

    


       
with tabs[6]:


    st.markdown(f"""
    <h1 style="
        text-align:center;
        background-color:#2563EB;   
        color:white;                
        padding:15px;               
        margin:20px 0;          
        border-radius:8px;          
        font-size:52px;             
    ">
    Raw Data & Download
    </h1>
""", unsafe_allow_html=True)

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="rwanda_exports_predictions.csv",
        mime="text/csv",
    )






    




    




  

    




