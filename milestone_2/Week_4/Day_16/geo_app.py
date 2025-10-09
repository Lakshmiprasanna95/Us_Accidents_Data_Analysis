# geo_app.py

import pandas as pd
import plotly.express as px
import streamlit as st

# --- File path ---
dataset_path = r"C:\Users\laksh\Downloads\US_Accidents_March23.csv"

# --- Columns we actually need ---
cols_to_use = [
    'ID', 'Start_Time', 'End_Time', 'State', 'Severity', 
    'Start_Lat', 'Start_Lng', 'Weather_Condition'
]

# --- Memory optimization: specify smaller data types ---
dtype_dict = {
    'Severity': 'int8',
    'State': 'category',
    'Weather_Condition': 'category'
}

# --- Function to read dataset in chunks and return a smaller DataFrame for plotting ---
def load_data(path, chunksize=100000, nrows=None):
    chunk_list = []
    total_rows = 0
    
    for chunk in pd.read_csv(path, usecols=cols_to_use, dtype=dtype_dict, chunksize=chunksize):
        chunk_list.append(chunk)
        total_rows += len(chunk)
        if nrows and total_rows >= nrows:
            break
    
    # Concatenate all chunks and limit rows if nrows specified
    df = pd.concat(chunk_list, ignore_index=True)
    if nrows:
        df = df.head(nrows)
    return df

# --- Load first 200,000 rows safely ---
df = load_data(dataset_path, chunksize=100000, nrows=200000)

st.title("US Accidents Analysis")

# --- Sidebar filter ---
state_options = df['State'].unique().tolist()
selected_state = st.sidebar.multiselect("Select State(s)", state_options, default=state_options[:5])

# Filter the data
filtered_df = df[df['State'].isin(selected_state)]

# --- Plot: Severity counts by State ---
severity_counts = filtered_df.groupby(['State', 'Severity']).size().reset_index(name='Count')

fig = px.bar(
    severity_counts,
    x='State',
    y='Count',
    color='Severity',
    barmode='group',
    title='Accident Severity by State'
)

st.plotly_chart(fig)

# --- Optional: show map of accidents ---
st.subheader("Accident Locations Map")

# Sample max 5000 points for performance
map_sample = filtered_df.sample(min(5000, len(filtered_df)), random_state=42).copy()

# Rename columns to what Streamlit expects
map_sample.rename(columns={'Start_Lat': 'lat', 'Start_Lng': 'lon'}, inplace=True)

# Display map
st.map(map_sample[['lat', 'lon']])

