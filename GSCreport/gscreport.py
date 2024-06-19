import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Set the page layout to wide
st.set_page_config(layout="wide")

# Custom CSS for tooltips and other styling
st.markdown("""
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }

    .tooltip .tooltiptext {
        visibility: visible;
        width: 200px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 5px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Position above the text */
        left: 50%;
        margin-left: -100px;
        opacity: 1;
        transition: opacity 0.3s;
    }

    .centered {
        display: flex;
        justify-content: center;
    }

    .title {
        font-size: 2.5rem;
        text-align: center;
        color: #4CAF50;
    }

    .divider {
        height: 2px;
        background-color: #4CAF50;
        margin: 20px 0;
    }

    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='title'>Google Search Console Data Analysis</h1>", unsafe_allow_html=True)
# sample_image_path="C:/Users/HP/OneDrive/Desktop/Office/GSCreport/Screenshot 2024-06-19 150107.png"

with st.expander("Instructions"):
    st.subheader("How to Use It")
    st.markdown("""
    Your CSV file should contain the following columns:
    - query
    - clicks
    - impressions
    - ctr
    - position
                
    **Ensure the column names exactly match the ones specified above.**
    """)
    st.subheader("Sample CSV:")
    df = pd.read_csv("GSCreport/samplecsvgsc.csv")
    st.write(
    f"""
    <div style="height: 300px; width: 1000px; overflow: auto;">
    {df.to_html(index=False)}
    </div>
    """,
    unsafe_allow_html=True
    )
# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    search_console_data = pd.read_csv(uploaded_file)
    st.markdown("<h2 class='centered'>Uploaded GSC Data</h2>", unsafe_allow_html=True)
    st.write(search_console_data)
    search_console_data.columns = search_console_data.columns.str.lower()
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if search_console_data['ctr'].dtype == 'object':
        search_console_data['ctr'] = search_console_data['ctr'].str.replace('%', '').astype(float)

    # Calculate overall performance metrics
    total_clicks = search_console_data['clicks'].sum()
    total_impressions = search_console_data['impressions'].sum()
    average_ctr = search_console_data['ctr'].mean()
    average_position = search_console_data['position'].mean()
    
    overall_performance = {
        "Total Clicks": total_clicks,
        "Total Impressions": total_impressions,
        "Average CTR": average_ctr,
        "Average Position": average_position
    }
    
    st.markdown("<h2 class='centered'>Overall Performance Metrics</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Clicks", value=total_clicks)

    with col2:
        st.metric(label="Total Impressions", value=total_impressions)

    with col3:
        st.metric(label="Average CTR (%)", value=f"{average_ctr:.2f}")

    with col4:
        st.metric(label="Average Position", value=f"{average_position:.2f}")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    def plot_bar(data, title, xlabel, ylabel, color):
        plt.figure(figsize=(10, 6))
        data.plot(kind='bar', color=color)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)
    
    if 'query' in search_console_data.columns:
        st.markdown("<h2 class='centered'>Top Queries by Clicks</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        top_queries_clicks = search_console_data.groupby('query')['clicks'].sum().sort_values(ascending=False).head(10)
        with col1:
            st.write(top_queries_clicks)
        with col2:
            plot_bar(top_queries_clicks, 'Graph of Top Queries by Clicks', 'Query', 'Clicks', 'b')
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("<h2 class='centered'>Top Queries by Impressions</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        top_queries_impressions = search_console_data.groupby('query')['impressions'].sum().sort_values(ascending=False).head(10)
        with col1:
            st.write(top_queries_impressions)
        with col2:
            plot_bar(top_queries_impressions, 'Graph of Top Queries by Impressions', 'Query', 'Impressions', 'g')
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("<h2 class='centered'>Top Queries by CTR</h2>", unsafe_allow_html=True)
        top_queries_ctr = search_console_data.groupby('query')['ctr'].mean().sort_values(ascending=False).head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.write(top_queries_ctr)
        with col2:
            plot_bar(top_queries_ctr, 'Graph of Top Queries by CTR', 'Query', 'CTR', 'r')
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("<h2 class='centered'>Top Queries by Position</h2>", unsafe_allow_html=True)
        top_queries_position = search_console_data.groupby('query')['position'].mean().sort_values().head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.write(top_queries_position)
        with col2:
            plt.figure(figsize=(10, 6))
            top_queries_position.plot(kind='bar', color='purple')
            plt.title('Graph of Top Queries by Position')
            plt.xlabel('Query')
            plt.ylabel('Position')
            plt.xticks(rotation=45)
            plt.gca().invert_yaxis()  # Lower positions are better
            plt.grid(True)
            st.pyplot(plt)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if 'page' in search_console_data.columns:
        st.markdown("<h2 class='centered'>Top Pages by Clicks</h2>", unsafe_allow_html=True)
        top_pages_clicks = search_console_data.groupby('page')['clicks'].sum().sort_values(ascending=False).head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.write(top_pages_clicks)
        with col2:
            plot_bar(top_pages_clicks, 'Graph of Top Pages by Clicks', 'Page', 'Clicks', 'b')
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("<h2 class='centered'>Top Pages by Impressions</h2>", unsafe_allow_html=True)
        top_pages_impressions = search_console_data.groupby('page')['impressions'].sum().sort_values(ascending=False).head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.write(top_pages_impressions)
        with col2:
            plot_bar(top_pages_impressions, 'Graph of Top Pages by Impressions', 'Page', 'Impressions', 'g')
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("<h2 class='centered'>Top Pages by CTR</h2>", unsafe_allow_html=True)
        top_pages_ctr = search_console_data.groupby('page')['ctr'].mean().sort_values(ascending=False).head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.write(top_pages_ctr)
        with col2:
            plot_bar(top_pages_ctr, 'Graph of Top Pages by CTR', 'Page', 'CTR', 'r')
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("<h2 class='centered'>Top Pages by Position</h2>", unsafe_allow_html=True)
        top_pages_position = search_console_data.groupby('page')['position'].mean().sort_values().head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.write(top_pages_position)
        with col2:
            plt.figure(figsize=(10, 6))
            top_pages_position.plot(kind='bar', color='purple')
            plt.title('Graph of Top Pages by Position')
            plt.xlabel('Page')
            plt.ylabel('Position')
            plt.xticks(rotation=45)
            plt.gca().invert_yaxis()  # Lower positions are better
            plt.grid(True)
            st.pyplot(plt)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
