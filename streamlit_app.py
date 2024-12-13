import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("hour.csv")

# Preprocessing
from scipy.stats import zscore

data['z_scores'] = zscore(data['cnt'])
threshold = 3
data_no_outliers = data[data['z_scores'].abs() <= threshold]
datafix = data_no_outliers.drop(columns=['z_scores'])
datafix['dteday'] = pd.to_datetime(datafix['dteday'])

# Header Function
def create_header():
    st.markdown(
        """
        <div style="background-color:#AEC6CF;padding:10px;border-radius:10px;">
            <h1 style="color:#2F4F4F;text-align:center;">Dashboard Bike Sharing</h1>
            <p style="color:#2F4F4F;text-align:center;">Analisis dan Visualisasi Data Penggunaan Sepeda</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Boxplot Function
# Boxplot Function
def plot_boxplot(data):
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid", palette="pastel")
    # Palet warna kustom berdasarkan musim
    palette = sns.color_palette("pastel", n_colors=data['season'].nunique())
    sns.boxplot(
        x='season',
        y='cnt',
        data=data,
        palette=palette,
        showmeans=True,
        meanprops={
            "marker": "o", 
            "markerfacecolor": "gold", 
            "markeredgecolor": "black",
            "markersize": 10
        }
    )
    plt.title('Pengaruh Musim terhadap Penggunaan Sepeda', fontsize=16, fontweight='bold', color="darkblue")
    plt.xlabel('Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)', fontsize=12, color="darkgreen")
    plt.ylabel('Jumlah Pengguna Sepeda', fontsize=12, color="darkgreen")
    plt.xticks(ticks=[0, 1, 2, 3], labels=["Spring", "Summer", "Fall", "Winter"], fontsize=10, color="darkblue")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

    # Menambahkan interpretasi atau komentar setelah grafik
    st.markdown("""
    - Penggunaan sepeda paling tinggi terjadi pada musim panas dan gugur, sedangkan paling rendah pada musim semi.
    - Cuaca yang lebih hangat di musim panas dan gugur mungkin menjadi faktor utama peningkatan jumlah pengguna sepeda.
    - Adanya outlier di musim panas dan gugur menunjukkan bahwa beberapa hari memiliki aktivitas pengguna sepeda yang sangat tinggi, kemungkinan terkait dengan acara tertentu atau cuaca yang sangat mendukung.
    """)


# Scatter Plot Function
def plot_scatter(data):
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid", palette="muted")
    scatter = sns.scatterplot(x='temp', y='cnt', data=data, alpha=0.7, edgecolor='k', s=50)
    sns.regplot(x='temp', y='cnt', data=data, scatter=False, color='red', line_kws={'linewidth': 2})
    plt.title('Hubungan antara Suhu dan Jumlah Pengguna Sepeda', fontsize=16, weight='bold')
    plt.xlabel('Suhu (Ternormalisasi)', fontsize=12)
    plt.ylabel('Jumlah Pengguna Sepeda', fontsize=12)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    # Menambahkan anotasi
    max_temp = data['temp'].idxmax()
    plt.annotate(
        'Suhu Maksimum', 
        xy=(data.loc[max_temp, 'temp'], data.loc[max_temp, 'cnt']),
        xytext=(data.loc[max_temp, 'temp'] + 0.1, data.loc[max_temp, 'cnt'] + 500),
        arrowprops=dict(facecolor='black', shrink=0.05),
        fontsize=10, color='blue'
    )

    st.pyplot(plt)

    # Menambahkan interpretasi atau komentar setelah grafik
    st.markdown("""
    Secara keseluruhan, grafik ini menunjukkan bahwa suhu memainkan peran penting dalam menentukan jumlah pengguna sepeda, meskipun faktor lain mungkin juga memengaruhi pola penggunaan sepeda.
    """)

# RFM Calculation Function
def calculate_rfm(data):
    today_date = data['dteday'].max()
    rfm_season = data.groupby('season').agg(
        Recency=('dteday', lambda x: (today_date - x.max()).days),
        Frequency=('instant', 'count'),
        Monetary=('cnt', 'sum')
    ).reset_index()

    # Replace season codes with season names
    rfm_season['season'] = rfm_season['season'].replace({1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'})

    return rfm_season

# RFM Visualization Function
def plot_rfm(rfm):
    top_recency_season = rfm.nsmallest(5, 'Recency')
    top_frequency_season = rfm.nlargest(5, 'Frequency')
    top_monetary_season = rfm.nlargest(5, 'Monetary')

    fig, axes = plt.subplots(1, 3, figsize=(22, 6), sharey=False)
    fig.patch.set_facecolor('#333333')
    plt.subplots_adjust(wspace=0.5)

    sns.barplot(x=top_recency_season['season'], y=top_recency_season['Recency'], ax=axes[0], palette='Blues')
    axes[0].set_title('By Recency (days)', fontsize=14, color='white')
    
    sns.barplot(x=top_frequency_season['season'], y=top_frequency_season['Frequency'], ax=axes[1], palette='Greens')
    axes[1].set_title('By Frequency', fontsize=14, color='white')

    sns.barplot(x=top_monetary_season['season'], y=top_monetary_season['Monetary'], ax=axes[2], palette='Reds')
    axes[2].set_title('By Monetary', fontsize=14, color='white')

    for ax in axes:
        ax.set_facecolor('#333333')
        ax.tick_params(colors='white')
    
    fig.suptitle('Best Season Based on RFM Parameters', fontsize=16, color='white')
    st.pyplot(fig)

    # Menambahkan interpretasi atau komentar setelah grafik
    st.markdown("""
    Dari grafik yang ditampilkan, berikut adalah interpretasi dari Best Season on RFM Parameters

    1. Musim Semi:
  
    Pelanggan di musim ini baru saja melakukan transaksi terakhir (Recency = 0), tetapi total pengeluaran (Monetary) paling rendah, meskipun frekuensinya cukup tinggi.

    2. Musim Panas:

    Pelanggan di musim ini memiliki frekuensi transaksi yang sangat tinggi (Frequency = 4355) dan total pengeluaran yang signifikan (Monetary = 875227). Namun, pembelian terakhirnya sudah cukup lama (Recency = 194).

    3. Musim Gugur:

    Ini adalah musim terbaik secara keseluruhan, karena memiliki frekuensi tertinggi (Frequency = 4378) dan total pengeluaran tertinggi (Monetary = 963756). Namun, pelanggan sudah mulai jarang melakukan transaksi (Recency = 100).

    4. Musim Dingin:

    Musim ini memiliki pelanggan yang cukup aktif dengan Recency rendah (11 hari), meskipun frekuensinya adalah yang terendah (Frequency = 4167). Total pengeluaran di musim ini juga signifikan (Monetary = 787737).
    """)

# Main Function
def main():
    create_header()

    st.sidebar.header("Navigasi")
    analysis_type = st.sidebar.selectbox("Pilih Analisis", ["Boxplot", "Scatter Plot", "RFM Analysis"])

    if analysis_type == "Boxplot":
        st.subheader("Pengaruh Musim terhadap Penggunaan Sepeda")
        plot_boxplot(datafix)
    elif analysis_type == "Scatter Plot":
        st.subheader("Hubungan antara Suhu dan Jumlah Pengguna Sepeda")
        plot_scatter(datafix)
    elif analysis_type == "RFM Analysis":
        st.subheader("RFM Analysis Berdasarkan Musim")
        rfm_season = calculate_rfm(datafix)
        st.dataframe(rfm_season)
        plot_rfm(rfm_season)

if __name__ == "__main__":
    main()