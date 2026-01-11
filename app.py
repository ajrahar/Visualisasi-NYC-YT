"""
NYC Taxi Data Analysis - Streamlit Application
Aplikasi untuk analisis dan visualisasi data NYC Taxi dari Google Drive
"""

import warnings
warnings.filterwarnings('ignore', message='.*Arrow.*')
warnings.filterwarnings('ignore', message='.*Serialization.*')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from utils.data_loader import load_data_from_gdrive, prepare_taxi_data

# NYC Taxi Data Dictionary Mappings
PAYMENT_TYPE_MAP = {
    0: '0 - Flex Fare',
    1: '1 - Credit Card',
    2: '2 - Cash',
    3: '3 - No Charge',
    4: '4 - Dispute',
    5: '5 - Unknown',
    6: '6 - Voided Trip'
}

VENDOR_ID_MAP = {
    1: '1 - Creative Mobile Technologies',
    2: '2 - Curb Mobility',
    6: '6 - Myle Technologies',
    7: '7 - Helix'
}

RATECODE_ID_MAP = {
    1: '1 - Standard Rate',
    2: '2 - JFK',
    3: '3 - Newark',
    4: '4 - Nassau/Westchester',
    5: '5 - Negotiated Fare',
    6: '6 - Group Ride',
    99: '99 - Null/Unknown'
}

# Terjemahan kolom ke Bahasa Indonesia yang mudah dipahami
COLUMN_TRANSLATIONS = {
    'VendorID': 'Perusahaan Taxi',
    'tpep_pickup_datetime': 'Waktu Jemput',
    'tpep_dropoff_datetime': 'Waktu Turun',
    'pickup_datetime': 'Waktu Jemput',
    'dropoff_datetime': 'Waktu Turun',
    'passenger_count': 'Jumlah Penumpang',
    'trip_distance': 'Jarak Perjalanan (mil)',
    'RatecodeID': 'Jenis Tarif',
    'store_and_fwd_flag': 'Status Penyimpanan',
    'PULocationID': 'Lokasi Jemput',
    'DOLocationID': 'Lokasi Turun',
    'payment_type': 'Metode Pembayaran',
    'fare_amount': 'Tarif Dasar ($)',
    'extra': 'Biaya Tambahan ($)',
    'mta_tax': 'Pajak MTA ($)',
    'tip_amount': 'Tip ($)',
    'tolls_amount': 'Biaya Tol ($)',
    'improvement_surcharge': 'Biaya Perbaikan ($)',
    'total_amount': 'Total Pembayaran ($)',
    'congestion_surcharge': 'Biaya Kemacetan ($)',
    'airport_fee': 'Biaya Bandara ($)',
    'cbd_congestion_fee': 'Biaya Zona Kemacetan ($)',
    'pickup_latitude': 'Latitude Jemput',
    'pickup_longitude': 'Longitude Jemput',
    'dropoff_latitude': 'Latitude Turun',
    'dropoff_longitude': 'Longitude Turun'
}

# Deskripsi kolom untuk tooltip/info
COLUMN_DESCRIPTIONS = {
    'VendorID': 'Perusahaan penyedia layanan taxi yang mencatat perjalanan ini',
    'tpep_pickup_datetime': 'Waktu saat meteran taxi dimulai',
    'tpep_dropoff_datetime': 'Waktu saat meteran taxi dihentikan',
    'passenger_count': 'Jumlah penumpang dalam kendaraan',
    'trip_distance': 'Jarak perjalanan dalam mil yang dilaporkan oleh meteran',
    'RatecodeID': 'Jenis tarif yang berlaku (Standard, JFK, Newark, dll)',
    'payment_type': 'Cara pembayaran penumpang (Kartu Kredit, Tunai, dll)',
    'fare_amount': 'Tarif berdasarkan waktu dan jarak yang dihitung meteran',
    'extra': 'Biaya tambahan seperti biaya malam atau rush hour',
    'mta_tax': 'Pajak MTA yang otomatis ditambahkan',
    'tip_amount': 'Tip untuk sopir (hanya tercatat untuk pembayaran kartu kredit)',
    'tolls_amount': 'Total biaya tol yang dibayar selama perjalanan',
    'total_amount': 'Total yang ditagihkan ke penumpang (tidak termasuk tip tunai)',
    'congestion_surcharge': 'Biaya tambahan untuk mengurangi kemacetan',
    'airport_fee': 'Biaya khusus untuk penjemputan di bandara LaGuardia dan JFK',
    'cbd_congestion_fee': 'Biaya zona kemacetan MTA (mulai Januari 2025)'
}

# Page configuration
st.set_page_config(
    page_title="NYC Taxi Data Analysis",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚕 NYC Taxi Data Analysis Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # NYC Taxi themed emoji/icon instead of broken image
    st.markdown("# 🚕 NYC Taxi")
    st.markdown("### Dashboard")
    st.divider()
    st.title("⚙️ Konfigurasi")
    
    # Google Drive URL input
    st.subheader("📁 Sumber Data")
    
    # File loading mode
    load_mode = st.radio(
        "Mode Loading",
        ["Single File (Google Drive)", "Multiple Files (Upload Langsung)"],
        help="Pilih single file untuk 1 file dari Google Drive, atau multiple files untuk upload beberapa file sekaligus"
    )
    
    if load_mode == "Single File (Google Drive)":
        gdrive_url = st.text_input(
            "Google Drive URL",
            placeholder="https://drive.google.com/file/d/...",
            help="Masukkan link Google Drive yang berisi data NYC Taxi (CSV, Parquet, atau Excel)"
        )
        
        file_format = st.selectbox(
            "Format File",
            ["csv", "parquet", "xlsx"],
            help="Pilih format file data Anda"
        )
        
        load_button = st.button("📥 Muat Data", type="primary", use_container_width=True)
        uploaded_files = None
    else:
        st.info("📂 **Upload Multiple Files untuk Auto-Merge**")
        st.markdown("""
        **Cara menggunakan:**
        1. Pilih semua file yang ingin digabungkan (Ctrl/Cmd + Click)
        2. Upload sekaligus
        3. Isi metadata periode data (opsional)
        4. Dashboard akan otomatis merge semua file
        5. Cocok untuk data 1 tahun penuh (12 file bulanan)
        """)
        
        uploaded_files = st.file_uploader(
            "Upload Files (CSV atau Parquet)",
            type=["csv", "parquet"],
            accept_multiple_files=True,
            help="Pilih beberapa file sekaligus untuk di-merge"
        )
        
        # Metadata untuk periode data
        st.subheader("📅 Metadata Periode Data (Opsional)")
        
        metadata_mode = st.radio(
            "Tipe Periode",
            ["Auto-detect dari data", "Manual - Bulan & Tahun", "Manual - Rentang Tanggal"],
            help="Pilih bagaimana periode data ditentukan"
        )
        
        data_period_info = None
        
        if metadata_mode == "Manual - Bulan & Tahun":
            col1, col2 = st.columns(2)
            with col1:
                start_month = st.selectbox(
                    "Bulan Awal",
                    ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                     "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
                    index=0
                )
            with col2:
                start_year = st.number_input("Tahun Awal", min_value=2000, max_value=2030, value=2023)
            
            if uploaded_files and len(uploaded_files) > 1:
                col3, col4 = st.columns(2)
                with col3:
                    end_month = st.selectbox(
                        "Bulan Akhir",
                        ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                         "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
                        index=11
                    )
                with col4:
                    end_year = st.number_input("Tahun Akhir", min_value=2000, max_value=2030, value=2023)
                
                data_period_info = {
                    'type': 'month_range',
                    'start_month': start_month,
                    'start_year': start_year,
                    'end_month': end_month,
                    'end_year': end_year
                }
            else:
                data_period_info = {
                    'type': 'single_month',
                    'month': start_month,
                    'year': start_year
                }
        
        elif metadata_mode == "Manual - Rentang Tanggal":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Tanggal Awal", value=pd.to_datetime('2023-01-01'))
            with col2:
                end_date = st.date_input("Tanggal Akhir", value=pd.to_datetime('2023-12-31'))
            
            data_period_info = {
                'type': 'date_range',
                'start_date': start_date,
                'end_date': end_date
            }
        else:
            data_period_info = {
                'type': 'auto_detect'
            }
        
        load_button = False
        gdrive_url = ""
        file_format = "parquet"
        
        if uploaded_files and len(uploaded_files) > 0:
            st.success(f"✅ {len(uploaded_files)} file siap untuk di-merge!")
            for i, file in enumerate(uploaded_files, 1):
                st.write(f"{i}. {file.name} ({file.size / 1024 / 1024:.2f} MB)")
    
    st.divider()
    
    # Sample data option
    st.subheader("🧪 Data Sample")
    use_sample = st.checkbox("Gunakan data sample untuk demo")
    
    if use_sample:
        st.info("💡 Mode demo akan menggunakan data sample yang sudah tersedia")

# Initialize session state EARLY to avoid SessionInfo errors
if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_period' not in st.session_state:
    st.session_state.data_period = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

def apply_data_mappings(df):
    """Apply NYC Taxi data dictionary mappings to dataframe"""
    df_mapped = df.copy()
    
    # Map payment_type
    if 'payment_type' in df_mapped.columns:
        df_mapped['payment_type'] = df_mapped['payment_type'].map(PAYMENT_TYPE_MAP).fillna(df_mapped['payment_type'].astype(str))
    
    # Map VendorID
    if 'VendorID' in df_mapped.columns:
        df_mapped['VendorID'] = df_mapped['VendorID'].map(VENDOR_ID_MAP).fillna(df_mapped['VendorID'].astype(str))
    
    # Map RatecodeID
    if 'RatecodeID' in df_mapped.columns:
        df_mapped['RatecodeID'] = df_mapped['RatecodeID'].map(RATECODE_ID_MAP).fillna(df_mapped['RatecodeID'].astype(str))
    
    return df_mapped

# Load data
if load_button and gdrive_url:
    output_file = f"nyc_taxi_data.{file_format}"
    df = load_data_from_gdrive(gdrive_url, output_file)
    if df is not None:
        df = prepare_taxi_data(df)
        df = apply_data_mappings(df)
        st.session_state.df = df
elif use_sample:
    # Create sample data for demonstration
    np.random.seed(42)
    n_samples = 10000
    
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', periods=n_samples)
    sample_data = {
        'pickup_datetime': dates,
        'dropoff_datetime': dates + pd.to_timedelta(np.random.randint(5, 60, n_samples), unit='m'),
        'passenger_count': np.random.randint(1, 6, n_samples),
        'trip_distance': np.random.exponential(3, n_samples),
        'fare_amount': np.random.exponential(15, n_samples) + 5,
        'tip_amount': np.random.exponential(3, n_samples),
        'total_amount': np.random.exponential(20, n_samples) + 8,
        'payment_type': np.random.choice(['Credit Card', 'Cash', 'Mobile'], n_samples, p=[0.6, 0.3, 0.1]),
        'pickup_latitude': np.random.uniform(40.6, 40.9, n_samples),
        'pickup_longitude': np.random.uniform(-74.05, -73.75, n_samples),
        'dropoff_latitude': np.random.uniform(40.6, 40.9, n_samples),
        'dropoff_longitude': np.random.uniform(-74.05, -73.75, n_samples),
    }
    st.session_state.df = pd.DataFrame(sample_data)
    st.success("✅ Data sample berhasil dimuat!")
elif uploaded_files and len(uploaded_files) > 0:
    # Process multiple uploaded files
    try:
        st.info(f"🔄 Memproses {len(uploaded_files)} file...")
        
        dfs = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Membaca {uploaded_file.name}... ({i+1}/{len(uploaded_files)})")
            
            # Read file based on extension
            if uploaded_file.name.endswith('.csv'):
                df_temp = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.parquet'):
                df_temp = pd.read_parquet(uploaded_file)
            else:
                st.warning(f"⚠️ Skipping {uploaded_file.name} - format tidak didukung")
                continue
            
            dfs.append(df_temp)
            st.write(f"  ✓ {uploaded_file.name}: {len(df_temp):,} baris")
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        if dfs:
            status_text.text("Menggabungkan semua file...")
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Apply data preparation and mappings
            combined_df = prepare_taxi_data(combined_df)
            combined_df = apply_data_mappings(combined_df)
            
            st.session_state.df = combined_df
            
            # Save or auto-detect period metadata
            if data_period_info and data_period_info['type'] != 'auto_detect':
                st.session_state.data_period = data_period_info
            else:
                # Auto-detect from data
                datetime_cols = combined_df.select_dtypes(include=['datetime64']).columns.tolist()
                if datetime_cols:
                    first_col = datetime_cols[0]
                    min_date = combined_df[first_col].min()
                    max_date = combined_df[first_col].max()
                    st.session_state.data_period = {
                        'type': 'auto_detected',
                        'start_date': min_date,
                        'end_date': max_date,
                        'column': first_col
                    }
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            st.success(f"✅ Berhasil menggabungkan {len(uploaded_files)} file!")
            st.info(f"📊 Total data: {len(combined_df):,} baris dari {len(dfs)} file")
        else:
            st.error("❌ Tidak ada file yang berhasil dibaca")
            
    except Exception as e:
        st.error(f"❌ Error saat memproses file: {str(e)}")

# Main content
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Data Overview
    st.header("📊 Ringkasan Data")
    
    # Display period information if available
    if st.session_state.data_period:
        period_info = st.session_state.data_period
        if period_info['type'] == 'month_range':
            period_text = f"📅 Periode: {period_info['start_month']} {period_info['start_year']} - {period_info['end_month']} {period_info['end_year']}"
        elif period_info['type'] == 'single_month':
            period_text = f"📅 Periode: {period_info['month']} {period_info['year']}"
        elif period_info['type'] == 'date_range':
            period_text = f"📅 Periode: {period_info['start_date']} - {period_info['end_date']}"
        elif period_info['type'] == 'auto_detected':
            start = period_info['start_date'].strftime('%d %b %Y')
            end = period_info['end_date'].strftime('%d %b %Y')
            period_text = f"📅 Periode (Auto-detected): {start} - {end}"
        else:
            period_text = ""
        
        if period_text:
            st.info(period_text)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trips", f"{len(df):,}")
    
    with col2:
        if 'fare_amount' in df.columns:
            avg_fare = df['fare_amount'].mean()
            st.metric("Rata-rata Tarif", f"${avg_fare:.2f}")
        else:
            st.metric("Total Kolom", len(df.columns))
    
    with col3:
        if 'trip_distance' in df.columns:
            avg_distance = df['trip_distance'].mean()
            st.metric("Rata-rata Jarak", f"{avg_distance:.2f} miles")
        else:
            st.metric("Data Points", f"{df.size:,}")
    
    with col4:
        if 'total_amount' in df.columns:
            total_revenue = df['total_amount'].sum()
            st.metric("Total Pendapatan", f"${total_revenue:,.2f}")
        else:
            st.metric("Ukuran Data", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Insights Section - "Tahukah Anda?"
    st.subheader("💡 Tahukah Anda?")
    
    insights = []
    
    # Generate interesting insights
    if 'trip_distance' in df.columns:
        avg_distance = df['trip_distance'].mean()
        max_distance = df['trip_distance'].max()
        insights.append(f"🚗 Rata-rata jarak perjalanan taxi adalah **{avg_distance:.2f} mil** (~{avg_distance*1.6:.2f} km)")
        insights.append(f"🏁 Perjalanan terjauh mencapai **{max_distance:.2f} mil** (~{max_distance*1.6:.2f} km)!")
    
    if 'fare_amount' in df.columns:
        avg_fare = df['fare_amount'].mean()
        max_fare = df['fare_amount'].max()
        insights.append(f"💵 Tarif rata-rata adalah **${avg_fare:.2f}** per perjalanan")
        if max_fare > 100:
            insights.append(f"💰 Tarif tertinggi mencapai **${max_fare:.2f}** - mungkin perjalanan ke bandara!")
    
    if 'tip_amount' in df.columns:
        avg_tip = df[df['tip_amount'] > 0]['tip_amount'].mean() if (df['tip_amount'] > 0).any() else 0
        if avg_tip > 0:
            insights.append(f"🎁 Rata-rata tip yang diberikan adalah **${avg_tip:.2f}**")
            tip_percentage = (df['tip_amount'].sum() / df['total_amount'].sum() * 100) if 'total_amount' in df.columns else 0
            if tip_percentage > 0:
                insights.append(f"📊 Tip mencakup **{tip_percentage:.1f}%** dari total pendapatan")
    
    if 'passenger_count' in df.columns:
        avg_passengers = df['passenger_count'].mean()
        solo_trips = (df['passenger_count'] == 1).sum() / len(df) * 100
        insights.append(f"👥 Rata-rata **{avg_passengers:.1f} penumpang** per perjalanan")
        insights.append(f"🚶 **{solo_trips:.1f}%** perjalanan hanya 1 penumpang")
    
    if 'payment_type' in df.columns:
        payment_dist = df['payment_type'].value_counts()
        if len(payment_dist) > 0:
            top_payment = payment_dist.index[0]
            top_payment_pct = payment_dist.iloc[0] / len(df) * 100
            insights.append(f"💳 Metode pembayaran terpopuler: **{top_payment}** ({top_payment_pct:.1f}%)")
    
    # Datetime insights
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if datetime_cols:
        dt_col = datetime_cols[0]
        df_temp = df.copy()
        df_temp['hour'] = df_temp[dt_col].dt.hour
        df_temp['day_of_week'] = df_temp[dt_col].dt.day_name()
        
        busiest_hour = df_temp['hour'].mode()[0] if not df_temp['hour'].mode().empty else None
        if busiest_hour is not None:
            insights.append(f"⏰ Jam tersibuk adalah **{busiest_hour}:00** (pukul {busiest_hour}.00)")
        
        busiest_day = df_temp['day_of_week'].mode()[0] if not df_temp['day_of_week'].mode().empty else None
        if busiest_day:
            day_translation = {
                'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
                'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
            }
            insights.append(f"📅 Hari tersibuk adalah **{day_translation.get(busiest_day, busiest_day)}**")
    
    # Display insights in columns
    if insights:
        cols = st.columns(2)
        for i, insight in enumerate(insights[:6]):  # Show max 6 insights
            with cols[i % 2]:
                st.info(insight)
    
    # Data Preview
    with st.expander("👀 Preview Data", expanded=False):
        st.dataframe(df.head(100), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Info Dataset")
            st.write(f"- **Baris:** {len(df):,}")
            st.write(f"- **Kolom:** {len(df.columns)}")
            st.write(f"- **Memory:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        with col2:
            st.subheader("Tipe Data")
            st.write(df.dtypes.value_counts())
    
    # Filters
    st.header("🔍 Filter Data")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    # Date filter
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if datetime_cols:
        with filter_col1:
            date_col = st.selectbox("Kolom Tanggal", datetime_cols)
            if date_col:
                min_date = df[date_col].min().date()
                max_date = df[date_col].max().date()
                date_range = st.date_input(
                    "Rentang Tanggal",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                if len(date_range) == 2:
                    df = df[(df[date_col].dt.date >= date_range[0]) & 
                           (df[date_col].dt.date <= date_range[1])]
    
    # Numeric filters
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols and len(numeric_cols) > 0:
        with filter_col2:
            numeric_col = st.selectbox("Filter Numerik", ['None'] + numeric_cols)
            if numeric_col != 'None':
                min_val = float(df[numeric_col].min())
                max_val = float(df[numeric_col].max())
                value_range = st.slider(
                    f"Range {numeric_col}",
                    min_val, max_val, (min_val, max_val)
                )
                df = df[(df[numeric_col] >= value_range[0]) & 
                       (df[numeric_col] <= value_range[1])]
    
    # Categorical filter
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        with filter_col3:
            cat_col = st.selectbox("Filter Kategori", ['None'] + categorical_cols)
            if cat_col != 'None':
                unique_vals = df[cat_col].unique().tolist()
                selected_vals = st.multiselect(
                    f"Pilih {cat_col}",
                    unique_vals,
                    default=unique_vals
                )
                if selected_vals:
                    df = df[df[cat_col].isin(selected_vals)]
    
    st.info(f"📌 Data setelah filter: {len(df):,} baris")
    
    # Visualizations
    st.header("📈 Visualisasi Data")
    st.caption("Grafik interaktif untuk memahami pola perjalanan taxi di NYC")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribusi", "📉 Pola Waktu", "🗺️ Peta Lokasi", "💰 Analisis Keuangan"])
    
    with tab1:
        st.subheader("Distribusi Data Perjalanan")
        st.caption("Melihat sebaran data untuk memahami karakteristik perjalanan")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            if 'passenger_count' in df.columns:
                st.markdown("**Jumlah Penumpang per Perjalanan**")
                st.caption("Berapa banyak orang yang biasanya naik taxi?")
                fig = px.histogram(
                    df, 
                    x='passenger_count',
                    title='',
                    color_discrete_sequence=['#3b82f6'],
                    labels={'passenger_count': 'Jumlah Penumpang', 'count': 'Jumlah Perjalanan'}
                )
                fig.update_layout(bargap=0.1, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Add insight
                mode_passengers = df['passenger_count'].mode()[0] if not df['passenger_count'].mode().empty else 0
                st.info(f"ℹ️ Paling sering: **{int(mode_passengers)} penumpang** per perjalanan")
        
        with viz_col2:
            if 'payment_type' in df.columns:
                st.markdown("**Metode Pembayaran**")
                st.caption("Bagaimana penumpang membayar taxi?")
                payment_counts = df['payment_type'].value_counts()
                fig = px.pie(
                    values=payment_counts.values,
                    names=payment_counts.index,
                    title='',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
                
                # Add insight
                if len(payment_counts) > 0:
                    top_method = payment_counts.index[0]
                    top_pct = payment_counts.iloc[0] / len(df) * 100
                    st.info(f"ℹ️ Terpopuler: **{top_method}** ({top_pct:.1f}%)")
        
        if 'trip_distance' in df.columns:
            st.markdown("**Jarak Perjalanan**")
            st.caption("Seberapa jauh biasanya orang naik taxi? (dalam mil, 1 mil ≈ 1.6 km)")
            fig = px.histogram(
                df,
                x='trip_distance',
                nbins=50,
                title='',
                color_discrete_sequence=['#10b981'],
                labels={'trip_distance': 'Jarak (mil)', 'count': 'Jumlah Perjalanan'}
            )
            fig.update_layout(bargap=0.05, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Add insight
            median_distance = df['trip_distance'].median()
            st.info(f"ℹ️ Jarak tengah (median): **{median_distance:.2f} mil** (~{median_distance*1.6:.2f} km)")
    
    with tab2:
        st.subheader("Analisis Time Series")
        
        if datetime_cols:
            selected_datetime = st.selectbox("Pilih kolom waktu", datetime_cols, key='ts_col')
            
            # Trips over time
            df_time = df.copy()
            df_time['date'] = df_time[selected_datetime].dt.date
            trips_per_day = df_time.groupby('date').size().reset_index(name='trips')
            
            fig = px.line(
                trips_per_day,
                x='date',
                y='trips',
                title='Jumlah Trip per Hari',
                markers=True
            )
            fig.update_traces(line_color='#3b82f6')
            st.plotly_chart(fig, use_container_width=True)
            
            # Hourly pattern
            if selected_datetime in df.columns:
                df_time['hour'] = df_time[selected_datetime].dt.hour
                trips_per_hour = df_time.groupby('hour').size().reset_index(name='trips')
                
                fig = px.bar(
                    trips_per_hour,
                    x='hour',
                    y='trips',
                    title='Pola Trip per Jam',
                    color='trips',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Visualisasi Geographic")
        
        if all(col in df.columns for col in ['pickup_latitude', 'pickup_longitude']):
            # Sample data for performance
            sample_size = min(1000, len(df))
            df_sample = df.sample(sample_size)
            
            fig = px.scatter_mapbox(
                df_sample,
                lat='pickup_latitude',
                lon='pickup_longitude',
                color='fare_amount' if 'fare_amount' in df.columns else None,
                size='passenger_count' if 'passenger_count' in df.columns else None,
                hover_data=['fare_amount'] if 'fare_amount' in df.columns else None,
                title=f'Lokasi Pickup (Sample {sample_size} trips)',
                mapbox_style='open-street-map',
                zoom=10,
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📍 Data koordinat geografis tidak tersedia")
    
    with tab4:
        st.subheader("Analisis Finansial")
        
        fin_col1, fin_col2 = st.columns(2)
        
        with fin_col1:
            if 'fare_amount' in df.columns:
                fig = px.box(
                    df,
                    y='fare_amount',
                    title='Distribusi Tarif',
                    color_discrete_sequence=['#3b82f6']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with fin_col2:
            if 'tip_amount' in df.columns:
                fig = px.histogram(
                    df,
                    x='tip_amount',
                    nbins=50,
                    title='Distribusi Tip',
                    color_discrete_sequence=['#10b981']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        if all(col in df.columns for col in ['trip_distance', 'fare_amount']):
            fig = px.scatter(
                df.sample(min(1000, len(df))),
                x='trip_distance',
                y='fare_amount',
                title='Hubungan Jarak vs Tarif',
                trendline='ols',
                opacity=0.6
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.header("📋 Statistik Deskriptif")
    
    stat_tab1, stat_tab2 = st.tabs(["Numerik", "Kategorikal"])
    
    with stat_tab1:
        if numeric_cols:
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    with stat_tab2:
        if categorical_cols:
            for col in categorical_cols[:3]:  # Show first 3 categorical columns
                st.subheader(f"Distribusi: {col}")
                value_counts = df[col].value_counts().head(10)
                st.bar_chart(value_counts)

else:
    # Welcome screen
    st.info("👋 Selamat datang! Silakan masukkan URL Google Drive di sidebar atau gunakan data sample untuk memulai analisis.")
    
    st.markdown("""
    ### 🚀 Cara Menggunakan:
    
    1. **Upload data ke Google Drive**
       - Pastikan file dalam format CSV, Parquet, atau Excel
       - Set sharing permission ke "Anyone with the link"
    
    2. **Salin link sharing**
       - Klik kanan pada file → Get link
       - Salin URL yang muncul
    
    3. **Paste URL di sidebar**
       - Masukkan URL ke input field
       - Pilih format file yang sesuai
       - Klik "Muat Data"
    
    4. **Atau gunakan data sample**
       - Centang "Gunakan data sample untuk demo"
       - Data sample akan otomatis dimuat
    
    ### 📊 Fitur Dashboard:
    - ✅ Visualisasi interaktif dengan Plotly
    - ✅ Filter data dinamis
    - ✅ Analisis time series
    - ✅ Peta geografis
    - ✅ Statistik deskriptif
    - ✅ Analisis finansial
    """)
    
    # Show sample URL format
    with st.expander("💡 Contoh Format URL Google Drive"):
        st.code("https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0j/view?usp=sharing")
        st.code("https://drive.google.com/uc?id=1a2b3c4d5e6f7g8h9i0j")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🚕 NYC Taxi Data Analysis Dashboard | Built with Streamlit & Python</p>
    </div>
""", unsafe_allow_html=True)
