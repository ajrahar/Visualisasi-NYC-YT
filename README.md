# 🚕 NYC Taxi Data Analysis - Streamlit Dashboard

Aplikasi web interaktif untuk analisis dan visualisasi data NYC Taxi menggunakan Python Streamlit. Aplikasi ini dapat memuat data langsung dari Google Drive dan menyediakan berbagai visualisasi serta analisis data.

## ✨ Fitur

- 📥 **Load Data dari Google Drive** - Import data langsung dari Google Drive
- 📊 **Visualisasi Interaktif** - Grafik dan chart interaktif menggunakan Plotly
- 🔍 **Filter Data Dinamis** - Filter berdasarkan tanggal, nilai numerik, dan kategori
- 📈 **Analisis Time Series** - Pola trip per hari dan per jam
- 🗺️ **Visualisasi Geographic** - Peta lokasi pickup dan dropoff
- 💰 **Analisis Finansial** - Distribusi tarif, tip, dan revenue
- 📋 **Statistik Deskriptif** - Summary statistics lengkap
- 🧪 **Mode Demo** - Data sample untuk testing
- 🏷️ **Data Dictionary Mapping** - Label jelas untuk payment type, vendor, rate code

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

### Opsi 1: Menggunakan Data dari Google Drive

1. **Upload data NYC Taxi ke Google Drive**
   - Format yang didukung: CSV, Parquet, Excel (.xlsx, .xls)
   
2. **Set sharing permission**
   - Klik kanan pada file → "Share" atau "Get link"
   - Pilih "Anyone with the link can view"
   - Copy URL yang muncul

3. **Paste URL di aplikasi**
   - Buka aplikasi Streamlit
   - Di sidebar, paste URL Google Drive
   - Pilih format file (csv/parquet/xlsx)
   - Klik "Muat Data"

4. **Mulai analisis!**
   - Data akan otomatis dimuat dan divisualisasikan
   - Gunakan filter untuk eksplorasi data
   - Lihat berbagai tab untuk visualisasi berbeda

### Opsi 2: Menggunakan Data Sample

1. Di sidebar, centang "Gunakan data sample untuk demo"
2. Data sample akan otomatis dimuat
3. Cocok untuk testing dan demo aplikasi

### Opsi 3: Load Multiple Files (Full Year Data)

Jika Anda memiliki data dalam multiple files (misalnya 12 file untuk Jan-Dec 2023):

**Step 1: Merge Files di Google Colab**
```python
# Upload semua file ke Google Colab, lalu jalankan:
import pandas as pd
import glob

# List all parquet files
files = sorted(glob.glob('yellow_tripdata_2023-*.parquet'))
print(f"Found {len(files)} files")

# Read and combine
dfs = []
for file in files:
    print(f"Reading {file}...")
    df = pd.read_parquet(file)
    dfs.append(df)

# Combine all dataframes
combined = pd.concat(dfs, ignore_index=True)
print(f"Total rows: {len(combined):,}")

# Save combined file
combined.to_parquet('yellow_tripdata_2023_full.parquet')
```

**Step 2: Upload & Load**
1. Download file hasil merge dari Colab
2. Upload ke Google Drive
3. Gunakan "Opsi 1" untuk load file tersebut

## 📊 Format Data yang Diharapkan

Aplikasi ini dirancang untuk data NYC Taxi dengan kolom-kolom seperti:

- `pickup_datetime` - Waktu pickup
- `dropoff_datetime` - Waktu dropoff
- `passenger_count` - Jumlah penumpang
- `trip_distance` - Jarak perjalanan (miles)
- `fare_amount` - Tarif dasar
- `tip_amount` - Jumlah tip
- `total_amount` - Total pembayaran
- `payment_type` - Metode pembayaran
- `pickup_latitude`, `pickup_longitude` - Koordinat pickup
- `dropoff_latitude`, `dropoff_longitude` - Koordinat dropoff

**Note:** Aplikasi akan tetap berfungsi meskipun tidak semua kolom tersedia. Visualisasi akan menyesuaikan dengan kolom yang ada.

## 🎨 Fitur Dashboard

### 1. Ringkasan Data
- Total trips
- Rata-rata tarif
- Rata-rata jarak
- Total revenue

### 2. Filter Data
- Filter berdasarkan rentang tanggal
- Filter nilai numerik (slider)
- Filter kategori (multiselect)

### 3. Visualisasi

#### Tab Distribusi
- Histogram jumlah penumpang
- Pie chart metode pembayaran
- Distribusi jarak perjalanan

#### Tab Time Series
- Jumlah trip per hari
- Pola trip per jam
- Trend analysis

#### Tab Geographic
- Scatter map lokasi pickup
- Visualisasi dengan Mapbox

#### Tab Financial
- Box plot distribusi tarif
- Histogram tip
- Scatter plot jarak vs tarif

### 4. Statistik Deskriptif
- Summary statistics untuk kolom numerik
- Distribusi untuk kolom kategorikal

## 🔧 Struktur Project

```
first/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── README.md             # Documentation (file ini)
└── utils/
    └── data_loader.py    # Google Drive data loading utilities
```

## 📦 Dependencies

- `streamlit` - Framework web app
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `plotly` - Interactive visualizations
- `matplotlib` - Static visualizations
- `seaborn` - Statistical visualizations
- `gdown` - Google Drive file downloader
- `openpyxl` - Excel file support
- `statsmodels` - Statistical modeling (untuk trendline)
- `requests` - HTTP library (fallback download)
- `urllib3` - HTTP client (downgraded untuk compatibility)

## 💡 Tips

1. **Untuk dataset besar**: Aplikasi menggunakan caching untuk performa optimal
2. **Visualisasi map**: Dibatasi 1000 sample untuk performa
3. **Format URL Google Drive**: 
   - `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
   - `https://drive.google.com/uc?id=FILE_ID`

## 🐛 Troubleshooting

### Error saat download dari Google Drive
- Pastikan file sharing permission sudah diset ke "Anyone with the link"
- Coba gunakan format URL yang berbeda
- Pastikan file tidak terlalu besar (max ~100MB untuk performa optimal)

### Visualisasi tidak muncul
- Periksa apakah kolom yang diperlukan ada di dataset
- Refresh browser (Ctrl+R atau Cmd+R)
- Restart aplikasi Streamlit

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
- `1` - Credit Card
- `2` - Cash
- `3` - No Charge
- `4` - Dispute
- `5` - Unknown
- `6` - Voided Trip

### Vendor ID
- `1` - Creative Mobile Technologies
- `2` - Curb Mobility
- `6` - Myle Technologies
- `7` - Helix

### Rate Code ID
- `1` - Standard Rate
- `2` - JFK
- `3` - Newark
- `4` - Nassau/Westchester
- `5` - Negotiated Fare
- `6` - Group Ride
- `99` - Null/Unknown

**Note:** Aplikasi otomatis mengkonversi kode numerik menjadi label yang mudah dibaca!

## 📝 Contoh Dataset NYC Taxi

Anda bisa mendapatkan dataset NYC Taxi dari:
- [NYC Taxi & Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Kaggle NYC Taxi Dataset](https://www.kaggle.com/c/nyc-taxi-trip-duration)

## 🤝 Kontribusi

Feel free to fork, modify, dan improve aplikasi ini sesuai kebutuhan Anda!

## 📄 License

MIT License - Bebas digunakan untuk keperluan pribadi maupun komersial.

---

**Dibuat dengan ❤️ menggunakan Streamlit & Python**
