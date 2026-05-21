import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import asyncio
import plotly.express as px
import pandas as pd
from app.graph.builder import get_graph
import uuid

st.set_page_config(page_title="Agentic Travel Assistant", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("<h1>Atlas</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>An intelligent travel assistant that combines destination insights, weather forecasting, and visual exploration through an agentic workflow.</p>", unsafe_allow_html=True)

# Initialize session state for thread_id to persist LangGraph memory
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# --- Search Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    query = st.text_input("Search", label_visibility="collapsed", placeholder="e.g., Tell me about Tokyo and what the weather is like next week.")
    
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
    with b_col2:
        explore_btn = st.button("Explore", use_container_width=True, type="primary")

# --- Results Section ---
if explore_btn:
    if query:
        with st.spinner("Agents are gathering information..."):
            app_graph = get_graph()
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            
            try:
                
                result = asyncio.run(app_graph.ainvoke({"user_query": query}, config=config))
                
                city = result.get("city", "Unknown City")
                summary = result.get("city_summary", "No summary available.")
                weather = result.get("weather_forecast", [])
                images = result.get("image_urls", [])
                source = result.get("source", "Unknown")
                
                st.divider()
                
                # --- Destination Header ---
                st.markdown(f"## Destination: {city}")
                st.caption(f"Knowledge Source: **{source.replace('_', ' ').title()}**")
                
                # --- Summary Card ---
                with st.container(border=True):
                    st.info(summary)
                
                st.write("") 
                
                # --- Visuals & Data ---
                c1, c2 = st.columns([1, 1], gap="large")
                
                with c1:
                    st.subheader("7-Day Forecast")
                    if weather and weather[0].get("day") != "N/A":
                        df = pd.DataFrame(weather)
                        fig = px.line(df, x="day", y="temperature", 
                                      title="Temperature Trend (°C)", 
                                      markers=True,
                                      labels={"temperature": "Temp (°C)", "day": "Date"})
                        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0)) 
                        st.plotly_chart(fig, use_container_width=True)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("Weather data is currently unavailable.")
                        
                with c2:
                    st.subheader("Highlights")
                    if images:
                        for img in images:
                            st.image(img, use_container_width=True, caption=f"Vistas of {city}")
                    else:
                        st.warning("No images found for this city.")
                        
            except Exception as e:
                st.error(f"An error occurred while executing the graph: {str(e)}")
    else:
        st.warning("Please enter a travel query to get started.")
