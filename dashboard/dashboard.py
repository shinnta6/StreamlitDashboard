import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Seaborn theme for all plots
sns.set(style="whitegrid")

current_dir = os.path.dirname(os.path.abspath(__file__))
hours_file = os.path.join(current_dir, 'hours_data.csv')
days_file = os.path.join(current_dir, 'days_data.csv')

hours_data = pd.read_csv(hours_file)
days_data = pd.read_csv(days_file)

# Convert date columns to datetime
days_data['dteday'] = pd.to_datetime(days_data['dteday'])
hours_data['dteday'] = pd.to_datetime(hours_data['dteday'])

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", 
                           ["Introduction & General Statistics", 
                            "Weather Impact on Rentals", 
                            "Rental Patterns", 
                            "Rentals per Hour Categories"])

# Date input for filtering
if section == "Introduction & General Statistics":
    st.sidebar.header("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2011-01-01'))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime('2012-12-31'))

    # Filter data based on date input
    filtered_days_data = days_data[(days_data['dteday'] >= pd.to_datetime(start_date)) & (days_data['dteday'] <= pd.to_datetime(end_date))]
    filtered_hours_data = hours_data[(hours_data['dteday'] >= pd.to_datetime(start_date)) & (hours_data['dteday'] <= pd.to_datetime(end_date))]
else:
    filtered_days_data = days_data
    filtered_hours_data = hours_data

if section == "Introduction & General Statistics":
    st.title("🚴‍♂️ Bike Sharing Data Analysis Dashboard")
    st.markdown("""
    Welcome to the Bike Sharing Dashboard. This dashboard provides insights into bike sharing patterns, 
    including weather influences and bike rental trends across different times of day and week.
    """)
    
    st.header("📊 General Statistics")
    
    # Calculate statistics
    total_rentals = filtered_days_data['cnt'].sum()
    total_casual = filtered_days_data['casual'].sum()
    total_registered = filtered_days_data['registered'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Rentals", value=f"{total_rentals:,}")
    
    with col2:
        st.metric(label="Casual Rentals", value=f"{total_casual:,}")
    
    with col3:
        st.metric(label="Registered Rentals", value=f"{total_registered:,}")
    
    # Trends Over Time
    st.subheader("📈 Trends Over Time")
    time_frame = st.radio("Select Time Frame:", ('Monthly', 'Weekly'))

    if time_frame == 'Monthly':
        # Monthly Rentals
        filtered_days_data['month'] = filtered_days_data['dteday'].dt.to_period('M')
        rentals_by_month = filtered_days_data.groupby('month')['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='month', y='cnt', data=rentals_by_month, palette='viridis', ax=ax)
        ax.set_title('Total Rentals per Month', fontsize=16)
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Total Rentals', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        
    else:
        # Weekly Rentals
        filtered_days_data.set_index('dteday', inplace=True)
        rentals_by_week = filtered_days_data['cnt'].resample('W').sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='dteday', y='cnt', data=rentals_by_week, palette='viridis', ax=ax)
        ax.set_title('Total Rentals per Week', fontsize=16)
        ax.set_xlabel('Week', fontsize=12)
        ax.set_ylabel('Total Rentals', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    
    # Average Rentals by Hour
    st.subheader("⏰ Average Rentals by Hour")
    average_rentals_by_hour = filtered_hours_data.groupby('hr')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='hr', y='cnt', data=average_rentals_by_hour, palette='viridis', ax=ax)
    ax.set_title('Average Rentals per Hour', fontsize=16)
    ax.set_xlabel('Hour', fontsize=12)
    ax.set_ylabel('Average Rentals', fontsize=12)
    st.pyplot(fig)
    
    # Weather Condition Breakdown
    st.subheader("☀️ Weather Condition Breakdown")
    weather_breakdown = filtered_days_data['weathersit'].value_counts(normalize=True) * 100
    weather_labels = weather_breakdown.index.map({1: 'Clear', 2: 'Misty', 3: 'Light Snow/Rain'})
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(weather_breakdown, labels=weather_labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(weather_labels)))
    ax.set_title('Rental Distribution by Weather Condition', fontsize=16)
    st.pyplot(fig)

# Section: Weather Impact on Rentals
if section == "Weather Impact on Rentals":
    st.header("🌦 Weather Impact on Bike Rentals")
    st.write("""
    Explore how different weather conditions influence the number of bike rentals. You can observe the correlation between weather factors and bike rentals.
    """)

    # Correlation Heatmap
    weather_data = days_data[['temp', 'hum', 'windspeed', 'weathersit', 'cnt']]
    corr_matrix = weather_data.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, annot_kws={"size": 10}, ax=ax)
    ax.set_title('Correlation Between Weather Factors and Bike Rentals', fontsize=16)
    st.pyplot(fig)

    # Scatter plots for weather factors
    st.subheader("📊 Bike Rentals vs Weather Factors")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.scatterplot(x='temp', y='cnt', data=days_data, color="blue", ax=ax)
        ax.set_title('Temperature vs Rentals')
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.scatterplot(x='hum', y='cnt', data=days_data, color="green", ax=ax)
        ax.set_title('Humidity vs Rentals')
        st.pyplot(fig)

    with col3:
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.scatterplot(x='windspeed', y='cnt', data=days_data, color="red", ax=ax)
        ax.set_title('Windspeed vs Rentals')
        st.pyplot(fig)

# Section: Rental Patterns
if section == "Rental Patterns":
    st.header("📅 Weekday vs Weekend Rentals")
    st.write("""
    Compare the rental patterns between weekdays and weekends. This section highlights the differences in bike rental activity based on the day of the week.
    """)

    # Barplot: Weekday vs Weekend Rentals
    workingday_trend = hours_data.groupby('workingday')['cnt'].sum().reset_index()
    workingday_trend['workingday'] = workingday_trend['workingday'].map({0: 'Weekend', 1: 'Weekday'})

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='workingday', y='cnt', data=workingday_trend, palette='coolwarm', ax=ax)
    ax.set_title('Total Rentals: Weekdays vs Weekends', fontsize=16)
    st.pyplot(fig)

    # Hourly Rentals Line Plot
    st.subheader("⏰ Hourly Rental Patterns")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', hue='workingday', data=hours_data, marker='o', palette='coolwarm', ax=ax)
    ax.set_title('Hourly Rentals: Weekdays vs Weekends', fontsize=16)
    st.pyplot(fig)

# Rentals per Hour Categories
if section == "Rentals per Hour Categories":
    st.header("⏳ Rental Patterns by Hour")
    st.write("""
    Analyze bike rentals across different time categories (Night, Morning, Afternoon, Evening). This analysis helps identify when the rental activity is highest throughout the day.
    """)
    
    # Binning the hour into categories
    hour_bins = [0, 6, 12, 18, 24]
    hour_labels = ['Night', 'Morning', 'Afternoon', 'Evening']
    hours_data['hour_binned'] = pd.cut(hours_data['hr'], bins=hour_bins, labels=hour_labels, include_lowest=True)

    binned_data = hours_data.groupby('hour_binned')[['cnt', 'casual', 'registered']].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    x = range(len(binned_data))

    # Plot the average rentals
    plt.bar(x, binned_data['cnt'], width=bar_width, label='Total Rentals', color='blue', align='center')
    plt.bar([p + bar_width for p in x], binned_data['casual'], width=bar_width, label='Casual Rentals', color='red', align='center')
    plt.bar([p + bar_width * 2 for p in x], binned_data['registered'], width=bar_width, label='Registered Rentals', color='green', align='center')
    plt.title('Average Bike Rentals by Time of Day (Binned)', fontsize=16)
    plt.xlabel('Time of Day', fontsize=12)
    plt.ylabel('Average Rentals', fontsize=12)
    plt.xticks([p + bar_width for p in x], binned_data['hour_binned'])
    plt.legend()
    st.pyplot(fig)
