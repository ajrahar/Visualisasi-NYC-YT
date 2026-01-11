# 🚕 NYC Taxi Data Analysis - Streamlit Dashboard

Aplikasi web interaktif untuk analisis dan visualisasi data NYC Taxi menggunakan Python Streamlit. Aplikasi ini dapat memuat data dari berbagai sumber dan menyediakan berbagai visualisasi serta analisis data yang mudah dipahami.

## ✨ Fitur Utama

### 📥 Multiple Data Loading Options
- **Google Drive** - Import data langsung dari Google Drive
- **Upload Lokal** - Upload file langsung dari komputer Anda
- **Multi-File Upload** - Upload dan merge beberapa file sekaligus
- **Sample Data** - Data demo untuk testing

### 📊 Visualisasi & Analisis
- **Visualisasi Interaktif** - Grafik interaktif menggunakan Plotly
- **Insights Otomatis** - "Tahukah Anda?" dengan fakta menarik dari data
- **Filter Data Dinamis** - Filter berdasarkan tanggal, nilai numerik, dan kategori
- **Analisis Time Series** - Pola trip per hari dan per jam
- **Visualisasi Geographic** - Peta lokasi pickup dan dropoff
- **Analisis Finansial** - Distribusi tarif, tip, dan revenue
- **Statistik Deskriptif** - Summary statistics lengkap

### 🌏 User-Friendly Interface
- **Bahasa Indonesia** - Semua label dan penjelasan dalam bahasa Indonesia
- **Terjemahan Kolom** - Nama kolom teknis diterjemahkan ke bahasa awam
- **Metadata Periode** - Tracking bulan/tahun atau rentang tanggal data
- **NYC Taxi Data Dictionary** - Mapping otomatis untuk payment type, vendor, rate code

## 🛠️ Instalasi

### 1. Clone atau Download Project

```bash
cd your-project-directory
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```bash
python -m venv venv

# Aktivasi virtual environment
# Untuk macOS/Linux:
source venv/bin/activate

# Untuk Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Cara Menjalankan

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## 📖 Cara Menggunakan

### Opsi 1: Upload File dari Komputer (Paling Mudah!)

1. **Pilih mode "Single File (Upload Lokal)"** di sidebar
2. **Klik "Browse files"**
3. **Pilih file dari komputer** (CSV, Parquet, atau Excel)
4. **File otomatis dimuat** dan siap dianalisis!

**Keuntungan:**
- ✅ Paling cepat dan mudah
- ✅ Tidak perlu internet
- ✅ Tidak perlu upload ke Google Drive
- ✅ Drag & drop support

### Opsi 2: Menggunakan Data dari Google Drive

1. **Upload data NYC Taxi ke Google Drive**
   - Format yang didukung: CSV, Parquet, Excel (.xlsx, .xls)
   
2. **Set sharing permission**
   - Klik kanan pada file → "Share" atau "Get link"
   - Pilih "Anyone with the link can view"
   - Copy URL yang muncul

3. **Paste URL di aplikasi**
   - Pilih mode "Single File (Google Drive)"
   - Paste URL Google Drive
   - Pilih format file (csv/parquet/xlsx)
   - Klik "Muat Data"

4. **Mulai analisis!**
   - Data akan otomatis dimuat dan divisualisasikan
   - Gunakan filter untuk eksplorasi data
   - Lihat berbagai tab untuk visualisasi berbeda

### Opsi 3: Upload Multiple Files (Full Year Data)

Jika Anda memiliki data dalam multiple files (misalnya 12 file untuk Jan-Dec 2023):

1. **Pilih mode "Multiple Files (Upload Langsung)"**
2. **Select semua file** (Ctrl/Cmd + Click)
3. **Isi metadata periode** (opsional):
   - Auto-detect dari data
   - Manual - Bulan & Tahun (contoh: Januari 2023 - Desember 2023)
   - Manual - Rentang Tanggal (contoh: 2023-01-01 to 2023-12-31)
4. **Upload** - Dashboard otomatis merge semua file
5. **Analisis data gabungan!**

### Opsi 4: Menggunakan Data Sample

1. Di sidebar, centang "Gunakan data sample untuk demo"
2. Data sample akan otomatis dimuat (10,000 records)
3. Cocok untuk testing dan demo aplikasi

## 📊 Format Data yang Diharapkan

Aplikasi ini dirancang untuk data NYC Taxi dengan kolom-kolom seperti:

### Kolom Utama
- `tpep_pickup_datetime` / `pickup_datetime` - Waktu jemput
- `tpep_dropoff_datetime` / `dropoff_datetime` - Waktu turun
- `passenger_count` - Jumlah penumpang
- `trip_distance` - Jarak perjalanan (miles)
- `payment_type` - Metode pembayaran (0-6)

### Kolom Finansial
- `fare_amount` - Tarif dasar
- `extra` - Biaya tambahan
- `mta_tax` - Pajak MTA
- `tip_amount` - Jumlah tip
- `tolls_amount` - Biaya tol
- `total_amount` - Total pembayaran
- `congestion_surcharge` - Biaya kemacetan
- `airport_fee` - Biaya bandara
- `cbd_congestion_fee` - Biaya zona kemacetan (2025+)

### Kolom Lokasi
- `PULocationID` / `pickup_latitude`, `pickup_longitude` - Lokasi jemput
- `DOLocationID` / `dropoff_latitude`, `dropoff_longitude` - Lokasi turun

### Kolom Lainnya
- `VendorID` - Perusahaan taxi (1, 2, 6, 7)
- `RatecodeID` - Jenis tarif (1-6, 99)
- `store_and_fwd_flag` - Status penyimpanan

**Note:** Aplikasi akan tetap berfungsi meskipun tidak semua kolom tersedia. Visualisasi akan menyesuaikan dengan kolom yang ada.

## 🎨 Fitur Dashboard

### 1. Ringkasan Data
- Total perjalanan
- Rata-rata tarif
- Rata-rata jarak
- Total pendapatan
- **Periode data** (bulan/tahun atau rentang tanggal)

### 2. 💡 Tahukah Anda? (Insights Otomatis)
Dashboard otomatis generate insights menarik seperti:
- 🚗 Rata-rata jarak perjalanan (dalam mil dan km)
- 💵 Tarif rata-rata dan tertinggi
- 🎁 Rata-rata tip yang diberikan
- 👥 Pola jumlah penumpang
- ⏰ Jam tersibuk
- 📅 Hari tersibuk
- 💳 Metode pembayaran terpopuler

### 3. Filter Data
- Filter berdasarkan rentang tanggal
- Filter nilai numerik (slider)
- Filter kategori (multiselect)
- Real-time data updates

### 4. Visualisasi (4 Tab)

#### Tab Distribusi
- Histogram jumlah penumpang (dengan insight)
- Pie chart metode pembayaran (dengan persentase)
- Distribusi jarak perjalanan (dengan median)

#### Tab Pola Waktu
- Line chart trips per hari
- Bar chart pola trips per jam
- Trend analysis

#### Tab Peta Lokasi
- Interactive scatter mapbox
- Visualisasi lokasi pickup
- Color-coded by fare amount

#### Tab Analisis Keuangan
- Box plot distribusi tarif
- Histogram tip amount
- Scatter plot jarak vs tarif dengan trendline

### 5. Statistik Deskriptif
- Summary statistics untuk kolom numerik
- Distribusi untuk kolom kategorikal
- Top 10 values per kategori

## 🔧 Struktur Project

```
your-project-directory/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
├── README.md                   # Documentation (file ini)
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── utils/
    └── data_loader.py         # Data loading utilities
```

## 📦 Dependencies

- `streamlit==1.31.0` - Framework web app
- `pandas==2.2.0` - Data manipulation
- `numpy==1.26.3` - Numerical operations
- `plotly==5.18.0` - Interactive visualizations
- `matplotlib==3.8.2` - Static visualizations
- `seaborn==0.13.1` - Statistical visualizations
- `gdown==4.7.1` - Google Drive file downloader
- `openpyxl==3.1.2` - Excel file support
- `statsmodels==0.14.1` - Statistical modeling (untuk trendline)
- `requests==2.32.5` - HTTP library (fallback download)
- `urllib3==1.26.18` - HTTP client (downgraded untuk compatibility)
- `pyarrow==14.0.1` - Arrow table support

## 💡 Tips & Best Practices

### Untuk Dataset Besar
- Aplikasi menggunakan caching untuk performa optimal
- Visualisasi map dibatasi 1000 sample untuk performa
- Gunakan format Parquet untuk file besar (lebih cepat dari CSV)

### Format URL Google Drive
```
✅ https://drive.google.com/file/d/FILE_ID/view?usp=sharing
✅ https://drive.google.com/uc?id=FILE_ID
```

### Upload File Lokal
- Recommended untuk file < 200MB
- Untuk file lebih besar, gunakan Google Drive
- Format Parquet paling efisien

### Multi-File Upload
- Cocok untuk data bulanan (12 file per tahun)
- Isi metadata periode untuk tracking yang lebih baik
- Auto-detect juga tersedia jika tidak yakin

## 🐛 Troubleshooting

### Error saat download dari Google Drive
- Pastikan file sharing permission sudah diset ke "Anyone with the link can view"
- Coba gunakan format URL yang berbeda
- Pastikan file tidak terlalu besar (max ~100MB untuk performa optimal)

### Visualisasi tidak muncul
- Periksa apakah kolom yang diperlukan ada di dataset
- Refresh browser (Ctrl+R atau Cmd+R)
- Restart aplikasi Streamlit

### Error saat upload file lokal
- Pastikan format file didukung (CSV, Parquet, Excel)
- Check ukuran file (recommended < 200MB)
- Pastikan file tidak corrupt

### Error saat install dependencies
```bash
# Upgrade pip terlebih dahulu
pip install --upgrade pip

# Install ulang dependencies
pip install -r requirements.txt
```

## 📝 NYC Taxi Data Dictionary

Aplikasi ini menggunakan mapping resmi dari NYC Taxi & Limousine Commission:

### Payment Type
- `0` - Flex Fare
- `1` - Credit Card (Kartu Kredit)
- `2` - Cash (Tunai)
- `3` - No Charge (Gratis)
- `4` - Dispute (Sengketa)
- `5` - Unknown (Tidak Diketahui)
- `6` - Voided Trip (Dibatalkan)

### Vendor ID
- `1` - Creative Mobile Technologies
- `2` - Curb Mobility
- `6` - Myle Technologies
- `7` - Helix

### Rate Code ID
- `1` - Standard Rate (Tarif Standar)
- `2` - JFK (Bandara JFK)
- `3` - Newark (Bandara Newark)
- `4` - Nassau/Westchester
- `5` - Negotiated Fare (Tarif Negosiasi)
- `6` - Group Ride (Perjalanan Grup)
- `99` - Null/Unknown

**Note:** Aplikasi otomatis mengkonversi kode numerik menjadi label yang mudah dibaca!

## 📝 Contoh Dataset NYC Taxi

Anda bisa mendapatkan dataset NYC Taxi dari:
- [NYC Taxi & Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Kaggle NYC Taxi Dataset](https://www.kaggle.com/c/nyc-taxi-trip-duration)

## 🌟 Fitur Unggulan

### 🇮🇩 Bahasa Indonesia
Semua interface dalam bahasa Indonesia yang mudah dipahami:
- Label kolom diterjemahkan (contoh: `trip_distance` → "Jarak Perjalanan (mil)")
- Penjelasan untuk setiap visualisasi
- Insights dalam bahasa sehari-hari
- Tooltips dan help text yang jelas

### 📅 Metadata Periode
Track periode data dengan 3 cara:
- **Auto-detect** - Otomatis dari tanggal min/max
- **Manual Bulan & Tahun** - Input bulan dan tahun (cocok untuk data bulanan)
- **Manual Rentang Tanggal** - Input tanggal awal dan akhir

### 💡 Insights Otomatis
Dashboard generate insights menarik seperti:
- Konversi otomatis mil ke km
- Persentase dan statistik yang mudah dipahami
- Fakta menarik tentang pola perjalanan
- Rekomendasi berdasarkan data

## 🤝 Kontribusi

Feel free to fork, modify, dan improve aplikasi ini sesuai kebutuhan Anda!

## 📄 License

MIT License - Bebas digunakan untuk keperluan pribadi maupun komersial.

---

**Dibuat dengan ❤️ menggunakan Streamlit & Python**

**Version:** 2.0.0  
**Last Updated:** January 2026  
**Features:** 3 Loading Modes | Indonesian Language | Auto Insights | Metadata Tracking
