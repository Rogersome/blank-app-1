import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import tempfile

# Title
st.title("Data Analysis and Model Training")

# File uploader for selecting database files
uploaded_files = st.file_uploader("Choose database files", type=["db"], accept_multiple_files=True)

# Function to display data from a database file
def display_data(file_name):
    con = sqlite3.connect(file_name)
    
    # Get all table names
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con)
    st.write("Tables found in database:", tables)
    
    for table_name in tables['name']:
        st.subheader(f"Table: {table_name}")
        try:
            # Use square brackets to handle special characters in table names
            query = f'SELECT * FROM [{table_name}]'
            data = pd.read_sql_query(query, con)
            st.write(data)
            
            # Display basic statistics
            st.write(data.describe())
            
            # Plotting options based on table schema
            columns = data.columns
            if table_name == 'Capacity_raw':
                plot_capacity_raw(data)
            elif table_name == 'EIS':
                plot_eis(data)
            elif table_name == 'OCV':
                plot_ocv(data)
            elif table_name == 'qOCV':
                plot_qocv(data)
        except Exception as e:
            st.error(f"Error reading table {table_name}: {e}")
        
    con.close()

# Plotting functions for each table
def plot_capacity_raw(data):
    st.subheader("Capacity_raw Plots")
    x_axis = st.selectbox("Select X-axis", data.columns, key='capacity_raw_x')
    y_axis = st.selectbox("Select Y-axis", data.columns, key='capacity_raw_y')
    if st.button("Generate Capacity_raw Plot"):
        fig = px.line(data, x=x_axis, y=y_axis, title=f"Capacity_raw: {x_axis} vs {y_axis}")
        st.plotly_chart(fig)

def plot_eis(data):
    st.subheader("EIS Plots")
    x_axis = st.selectbox("Select X-axis", data.columns, key='eis_x')
    y_axis = st.selectbox("Select Y-axis", data.columns, key='eis_y')
    if st.button("Generate EIS Plot"):
        fig = px.line(data, x=x_axis, y=y_axis, title=f"EIS: {x_axis} vs {y_axis}")
        st.plotly_chart(fig)

def plot_ocv(data):
    st.subheader("OCV Plots")
    x_axis = st.selectbox("Select X-axis", data.columns, key='ocv_x')
    y_axis = st.selectbox("Select Y-axis", data.columns, key='ocv_y')
    if st.button("Generate OCV Plot"):
        fig = px.line(data, x=x_axis, y=y_axis, title=f"OCV: {x_axis} vs {y_axis}")
        st.plotly_chart(fig)

def plot_qocv(data):
    st.subheader("qOCV Plots")
    x_axis = st.selectbox("Select X-axis", data.columns, key='qocv_x')
    y_axis = st.selectbox("Select Y-axis", data.columns, key='qocv_y')
    if st.button("Generate qOCV Plot"):
        fig = px.line(data, x=x_axis, y=y_axis, title=f"qOCV: {x_axis} vs {y_axis}")
        st.plotly_chart(fig)

# Display uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"File name: {uploaded_file.name}")
        
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_name = temp_file.name
        
        # Display data from the temporary file
        display_data(temp_file_name)

# Add model training and data analysis sections
st.header("Model Training")
st.write("This section will include model training steps.")
# Add more functionalities as needed