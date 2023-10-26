import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_filtered_day11_df(df):
    filtered_day11_df = df[df['yr'] == 0]
    sum_order11_df = filtered_day11_df.groupby(["yr", "mnth"]).cnt.sum().reset_index()
    return sum_order11_df

def create_filtered_day12_df(df):
    filtered_day12_df = df[df['yr'] == 1]
    sum_order12_df = filtered_day12_df.groupby(["yr", "mnth"]).cnt.sum().reset_index()
    return sum_order12_df

def create_filtered_monthAll_df(df):
    sum_rent_month_df = df.groupby("mnth").cnt.sum().reset_index()
    return sum_rent_month_df

def create_filtered_season_df(df):
    filtered_season_df = df.groupby(by="season").cnt.sum().reset_index()
    return filtered_season_df

def create_filtered_weather_df(df):
    filtered_weather_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    return filtered_weather_df

day_df = pd.read_csv("dashboard/day_df_clean.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])


# membuat filter 
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# menyimpan data filter
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# memanggil helper function 
filtered_day11_df = create_filtered_day11_df(main_df)
filtered_day12_df = create_filtered_day12_df(main_df)
filtered_monthAll_df = create_filtered_monthAll_df(main_df)
filtered_season_df = create_filtered_season_df(main_df)
filtered_weather_df = create_filtered_weather_df(main_df)

# memberi header dashboard
st.header('Rent Bike Analysis 🚴')

# menampilkan rata rata penjualan
st.subheader('Sales Statistics')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = filtered_day11_df.cnt.sum()
    st.metric("Total Orders 2011", value=total_orders)

with col2:
    total_orders = filtered_day12_df.cnt.sum()
    st.metric("Total Orders 2012", value=total_orders)


# membuat plot
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

# Plot untuk tahun 2011
ax1.plot(
    filtered_day11_df["mnth"],
    filtered_day11_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax1.tick_params(axis='y', labelsize=20)
ax1.tick_params(axis='x', labelsize=15)
ax1.set_title('Number of Customer in 2011', fontsize=20)
ax1.set_xlabel('Bulan', fontsize=20)
ax1.set_ylabel('Jumlah', fontsize=20)

# Plot untuk tahun 2012
ax2.plot(
    filtered_day12_df["mnth"],
    filtered_day12_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#F48FB1"
)
ax2.tick_params(axis='y', labelsize=20)
ax2.tick_params(axis='x', labelsize=15)
ax2.set_title('Number of Customer in 2012', fontsize=20)
ax2.set_xlabel('Bulan', fontsize=20)
ax2.set_ylabel('Jumlah', fontsize=20)

fig.subplots_adjust(wspace=0.4)

st.pyplot(fig)

st.subheader('Average Sales each Month')

# Rata rata tiap bulan
fig, ax = plt.subplots(figsize=(20, 10))

colors = ["#D3D3D3"] * len(filtered_monthAll_df) 
max_value_row11 = filtered_monthAll_df[filtered_monthAll_df['cnt'] == filtered_monthAll_df['cnt'].max()]
max_index11 = max_value_row11.index[0]
colors[max_index11] = "#72BCD4"

sns.barplot(
    x="mnth", 
    y="cnt",
    data=filtered_monthAll_df,
    palette=colors,
    ax=ax
)

ax.set_title("Number of Customer by Month", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.subheader('Sales Based on Seasonal and Weather Factors')

# rata-rata musim dan cuaca
col1, col2 = st.columns(2)

# musim
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3"] * len(filtered_season_df) 
    max_value_season = filtered_season_df[filtered_season_df['cnt'] == filtered_season_df['cnt'].max()]
    max_index_season = max_value_season.index[0]
    colors[max_index_season] = "#72BCD4"
 
    sns.barplot(
        y="cnt", 
        x="season",
        data=filtered_season_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# cuaca
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3"] * len(filtered_weather_df) 
    max_value_weather = filtered_weather_df[filtered_weather_df['cnt'] == filtered_weather_df['cnt'].max()]
    max_index_weather = max_value_weather.index[0]
    colors[max_index_weather] = "#72BCD4"
 
    sns.barplot(
        y="cnt", 
        x="weathersit",
        data=filtered_weather_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Weather", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
