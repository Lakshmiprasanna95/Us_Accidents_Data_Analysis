import pandas as pd
import plotly.express as px
import streamlit as st


dataset_path = r"C:\Users\laksh\Downloads\US_Accidents_March23.csv"

# Load dataset (you can limit rows if needed)
df = pd.read_csv(dataset_path, nrows=100000)

def plot_accidents_sampled(df, location_col='State', sample_size=50000):
    df_sample = df.sample(n=sample_size) if len(df) > sample_size else df

    fig = px.scatter(
        df_sample,
        x='Start_Lng',
        y='Start_Lat',
        color='Severity',
        size_max=10,
        hover_data=['ID', 'Start_Time', 'State', 'City']
    )
    st.plotly_chart(fig)

st.title('Accident Data Visualization')

location_options = st.selectbox("Select Location Type", ['State', 'City'])
plot_accidents_sampled(df, location_col=location_options)



#  Hypothesis Testing

# 1. What time of day has the most accidents?

# Convert Start_Time to datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['Hour'] = df['Start_Time'].dt.hour

# Count accidents per hour
accidents_by_hour = df['Hour'].value_counts().sort_index()

# Plot
fig1 = px.bar(
    x=accidents_by_hour.index,
    y=accidents_by_hour.values,
    labels={'x':'Hour of Day', 'y':'Number of Accidents'},
    title='Accidents by Hour of Day'
)
st.plotly_chart(fig1)

# 2. Are accidents more severe during rain or fog?

# Filter only rows where Weather_Condition mentions Rain or Fog
weather_filter = df['Weather_Condition'].str.contains('Rain|Fog', case=False, na=False)
df_weather = df[weather_filter]

# Severity counts by Weather_Condition
severity_by_weather = df_weather.groupby('Weather_Condition')['Severity'].mean().sort_values(ascending=False)

# Plot
fig2 = px.bar(
    x=severity_by_weather.index,
    y=severity_by_weather.values,
    labels={'x':'Weather Condition', 'y':'Average Severity'},
    title='Average Severity of Accidents During Rain or Fog'
)
st.plotly_chart(fig2)


