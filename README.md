# 🚴‍♂️🚴‍♀️🚴 Bike Sharing Dataset Analysis 🚴‍♂️🚴‍♀️🚴

Selamat datang di proyek analisis data **Bike Sharing Dataset**! ✨ Proyek ini berfokus pada eksplorasi dan analisis data perjalanan sepeda yang diambil dari dataset populer di Kaggle. Dengan memanfaatkan dataset ini, kita dapat mendapatkan wawasan mendalam tentang pola penggunaan sepeda, dampak cuaca, dan preferensi pengguna.

## 🔗 Tautan Penting

- **Dataset**: [Bike Sharing Dataset di Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)
- **Dashboard Interaktif**: [Bike Sharing Dashboard](https://bikesharingdashboard-zidnytaqiyaa.streamlit.app/)

## 📊 Tentang Dataset

Dataset ini mencatat informasi perjalanan sepeda yang dilakukan secara otomatis melalui sistem berbagi sepeda. Beberapa atribut utama yang tersedia meliputi:

- **Waktu**: Hari, bulan, musim, dan waktu dalam sehari.
- **Kondisi Cuaca**: Temperatur, kelembapan, kecepatan angin, dan tingkat cuaca.
- **Pengguna**: Jumlah pengguna kasual dan terdaftar.

## 🔍 Melalui analisis dataset ini, kita dapat:

1. Apakah ada pola musiman yang konsisten yang dapat dimanfaatkan untuk perencanaan operasional?

2. Apakah terdapat hubungan yang signifikan antara suhu dan jumlah pengguna sepeda?

3. Apakah terdapat hubungan yang signifikan antara waktu dalam sehari dan jumlah pengguna sepeda?

4. Apakah ada perbedaan signifikan dalam jumlah penyewaan sepeda antara tahun pertama (2011) dan tahun kedua (2012)?

5. Analisis RFM berdasarkan musim: Mengelompokkan pengguna untuk memahami perilaku dan preferensi berdasarkan frekuensi, nilai monetisasi, dan waktu sewa.


## ⚡ Cara Menjalankan Dashboard Streamlit di Google Colab

Untuk menjalankan dashboard ini di lingkungan Google Colab, ikuti langkah berikut:

1. **Instalasi Streamlit**:

   ```bash
   !pip install streamlit
   ```

2. **Jalankan Streamlit dan Localtunnel**:

   ```bash
   !streamlit run streamlit.py & npx localtunnel --port 8501
   ```

## 🌐 Teknologi yang Digunakan

- **Python**: Untuk analisis data dan pembuatan model.
- **Streamlit**: Untuk membuat dashboard interaktif.
- **Pandas & NumPy**: Untuk manipulasi data.
- **Matplotlib & Seaborn**: Untuk visualisasi data.
- **Scikit-learn**: Untuk prediksi dan analisis lanjutan (jika diperlukan).

## 🛠️ Instalasi Lokal

1. Clone repositori ini:

   ```bash
   git clone https://github.com/username/bike-sharing-analysis.git
   ```

2. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi Streamlit:

   ```bash
   streamlit run streamlit.py
   ```

## 🎉 Terima Kasih

Terima kasih telah mengunjungi proyek ini!

Mari kita jelajahi lebih dalam dunia berbagi sepeda dan temukan wawasan yang menarik bersama-sama! 🏍️

