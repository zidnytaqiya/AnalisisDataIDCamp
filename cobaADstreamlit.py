import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Judul Aplikasi
st.title("Analisis Data Penyewaan Sepeda")
st.sidebar.title("Navigasi")
st.sidebar.write("Gunakan menu untuk memilih analisis")

# Unggah data
uploaded_file = st.sidebar.file_uploader("Unggah file CSV", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("### Tampilan Data")
    st.write(data.head())

    # Informasi dasar
    st.subheader("Informasi Dataset")
    buffer = st.expander("Tampilkan Informasi Data")
    with buffer:
        buffer.write(data.info())

    # Analisis Outlier dengan Z-Score
    st.subheader("Analisis Outlier dengan Z-Score")
    threshold = st.slider("Threshold Outlier (Z-Score)", min_value=2, max_value=5, value=3)
    data['z_scores'] = zscore(data['cnt'])
    outliers = data[data['z_scores'].abs() > threshold]
    st.write(f"Jumlah Outlier: {outliers.shape[0]}")
    st.write(outliers)

    data_no_outliers = data[data['z_scores'].abs() <= threshold].drop(columns=['z_scores'])
    st.write("Data Tanpa Outlier:", data_no_outliers.shape[0])

    # Boxplot: Pengaruh Musim terhadap Penggunaan Sepeda
    st.subheader("Pengaruh Musim terhadap Penggunaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='season', y='cnt', data=data, palette="pastel", showmeans=True,
                meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "black"})
    ax.set_title("Pengaruh Musim terhadap Penggunaan Sepeda", fontsize=16, weight="bold")
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Jumlah Pengguna", fontsize=12)
    st.pyplot(fig)

    st.write("#### Pola Musiman")
    st.write(
        "Terdapat pola musiman yang konsisten dalam penggunaan sepeda, dengan puncak penggunaan pada musim panas dan gugur.")

    # Scatterplot: Hubungan Suhu dan Jumlah Pengguna Sepeda
    st.subheader("Hubungan antara Suhu dan Jumlah Pengguna Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', data=data, alpha=0.7, edgecolor='k', s=50, ax=ax)
    sns.regplot(x='temp', y='cnt', data=data, scatter=False, color='red', line_kws={'linewidth': 2}, ax=ax)
    ax.set_title("Hubungan Suhu dan Jumlah Pengguna", fontsize=16, weight="bold")
    st.pyplot(fig)

    st.write("#### Hubungan Suhu dan Pengguna")
    st.write("Terdapat hubungan signifikan antara suhu dan jumlah pengguna sepeda.")

    # Barplot: Rata-rata Penyewaan Berdasarkan Waktu
    st.subheader("Penyewaan Sepeda Berdasarkan Waktu dalam Sehari")

    def classify_time(hour):
        if 0 <= hour < 6:
            return 'Dini Hari'
        elif 6 <= hour < 12:
            return 'Pagi'
        elif 12 <= hour < 18:
            return 'Siang'
        else:
            return 'Malam'

    data['time_of_day'] = data['hr'].apply(classify_time)
    time_of_day_trend = data.groupby('time_of_day')['cnt'].mean().reset_index()
    time_of_day_trend['time_of_day'] = pd.Categorical(
        time_of_day_trend['time_of_day'], categories=['Dini Hari', 'Pagi', 'Siang', 'Malam'], ordered=True)
    time_of_day_trend = time_of_day_trend.sort_values('time_of_day')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='time_of_day', y='cnt', data=time_of_day_trend, palette='Set2', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Waktu", fontsize=16, weight="bold")
    st.pyplot(fig)

    st.write("#### Tren Waktu")
    st.write("Penyewaan sepeda lebih tinggi pada pagi dan siang hari.")

    # Line Plot: Penyewaan Sepeda Berdasarkan Bulan
    st.subheader("Tren Penyewaan Berdasarkan Bulan")
    monthly_data = data.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
    data_2011 = monthly_data[monthly_data['yr'] == 0]
    data_2012 = monthly_data[monthly_data['yr'] == 1]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data_2011['mnth'], data_2011['cnt'], label='2011', marker='o', color='#A1C6EA')
    ax.plot(data_2012['mnth'], data_2012['cnt'], label='2012', marker='o', color='#F4A9A8')
    ax.set_title("Tren Penyewaan Berdasarkan Bulan", fontsize=14, weight="bold")
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
    ax.legend()
    st.pyplot(fig)

    st.write("#### Tren Tahunan")
    st.write("Tahun kedua memiliki penyewaan yang lebih tinggi dibandingkan tahun pertama.")

    # RFM Analysis Berdasarkan Musim
    st.subheader("RFM Analysis Berdasarkan Musim")
    data['dteday'] = pd.to_datetime(data['dteday'])
    today_date = data['dteday'].max()
    rfm_season = data.groupby('season').agg(
        Recency=('dteday', lambda x: (today_date - x.max()).days),
        Frequency=('instant', 'count'),
        Monetary=('cnt', 'sum')
    ).reset_index()

    season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    rfm_season['season'] = rfm_season['season'].map(season_mapping)

    fig, axes = plt.subplots(1, 3, figsize=(24, 6))
    sns.barplot(x='season', y='Recency', data=rfm_season, palette='Blues', ax=axes[0])
    sns.barplot(x='season', y='Frequency', data=rfm_season, palette='Greens', ax=axes[1])
    sns.barplot(x='season', y='Monetary', data=rfm_season, palette='Reds', ax=axes[2])

    axes[0].set_title("Recency per Season")
    axes[1].set_title("Frequency per Season")
    axes[2].set_title("Monetary per Season")

    st.pyplot(fig)
    st.write("#### Ringkasan RFM")
    st.write(rfm_season)
