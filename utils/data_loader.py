"""
Utility functions for loading NYC Taxi data from Google Drive
"""
import streamlit as st
import pandas as pd
import gdown
import os
import re
from typing import Optional


@st.cache_data(ttl=3600)
def load_data_from_gdrive(gdrive_url: str, output_filename: str = "nyc_taxi_data.csv") -> Optional[pd.DataFrame]:
    """
    Download and load data from Google Drive
    
    Args:
        gdrive_url: Google Drive sharing URL
        output_filename: Name for the downloaded file
        
    Returns:
        DataFrame containing the data, or None if failed
    """
    try:
        # Extract file ID from Google Drive URL using regex
        file_id = None
        
        # Pattern 1: /file/d/FILE_ID/
        pattern1 = r'/file/d/([a-zA-Z0-9_-]+)'
        match1 = re.search(pattern1, gdrive_url)
        if match1:
            file_id = match1.group(1)
        
        # Pattern 2: id=FILE_ID
        if not file_id:
            pattern2 = r'id=([a-zA-Z0-9_-]+)'
            match2 = re.search(pattern2, gdrive_url)
            if match2:
                file_id = match2.group(1)
        
        # Pattern 3: /open?id=FILE_ID
        if not file_id:
            pattern3 = r'/open\?id=([a-zA-Z0-9_-]+)'
            match3 = re.search(pattern3, gdrive_url)
            if match3:
                file_id = match3.group(1)
        
        if not file_id:
            st.error("❌ Format URL Google Drive tidak valid. Pastikan URL berisi file ID yang benar.")
            st.info("""
            **Contoh format URL yang valid:**
            - https://drive.google.com/file/d/FILE_ID/view?usp=sharing
            - https://drive.google.com/open?id=FILE_ID
            - https://drive.google.com/uc?id=FILE_ID
            """)
            return None
        
        # Create download URL
        download_url = f"https://drive.google.com/uc?id={file_id}"
        
        st.info(f"📥 File ID terdeteksi: {file_id}")
        
        # Download file with better error handling
        with st.spinner("Mengunduh data dari Google Drive..."):
            try:
                # Try using gdown with fuzzy mode
                result = gdown.download(download_url, output_filename, quiet=False, fuzzy=True)
            except AttributeError as e:
                # If gdown fails with AttributeError, try alternative method
                st.warning("⚠️ Mencoba metode download alternatif...")
                try:
                    import requests
                    response = requests.get(download_url, allow_redirects=True)
                    if response.status_code == 200:
                        with open(output_filename, 'wb') as f:
                            f.write(response.content)
                        result = output_filename
                    else:
                        st.error(f"❌ Gagal download: HTTP {response.status_code}")
                        return None
                except Exception as req_error:
                    st.error(f"❌ Error saat download: {str(req_error)}")
                    return None
            except Exception as e:
                st.error(f"❌ Error dari gdown: {str(e)}")
                st.info("💡 Coba gunakan direct download link atau pastikan file accessible")
                return None
            
            if result is None or not os.path.exists(output_filename):
                st.error("❌ Gagal mengunduh file. Pastikan file dapat diakses secara publik (Anyone with the link can view).")
                st.info("💡 **Cara set permission:**")
                st.info("1. Buka file di Google Drive")
                st.info("2. Klik kanan → Share")
                st.info("3. Pilih 'Anyone with the link' → Viewer")
                st.info("4. Copy link dan paste di sini")
                return None
        
        # Load data based on file extension
        st.info(f"📂 Memuat file: {output_filename}")
        
        if output_filename.endswith('.csv'):
            df = pd.read_csv(output_filename)
        elif output_filename.endswith('.parquet'):
            df = pd.read_parquet(output_filename)
        elif output_filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(output_filename)
        else:
            st.error("Format file tidak didukung. Gunakan CSV, Parquet, atau Excel.")
            return None
        
        # Clean up downloaded file (optional - comment out if you want to keep it)
        # os.remove(output_filename)
        
        st.success(f"✅ Data berhasil dimuat! {len(df):,} baris dan {len(df.columns)} kolom")
        return df
        
    except Exception as e:
        st.error(f"❌ Error saat memuat data: {str(e)}")
        st.info("💡 **Tips troubleshooting:**")
        st.info("1. Pastikan file sharing permission diset ke 'Anyone with the link can view'")
        st.info("2. Coba copy URL langsung dari tombol 'Share' di Google Drive")
        st.info("3. Pastikan file tidak terlalu besar (recommended < 100MB)")
        return None


@st.cache_data
def prepare_taxi_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare and clean NYC Taxi data
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame with Arrow-compatible dtypes
    """
    df_clean = df.copy()
    
    # Fix Arrow compatibility - convert to standard pandas dtypes
    for col in df_clean.columns:
        # Handle numeric columns
        if pd.api.types.is_float_dtype(df_clean[col]):
            # Convert to nullable float to avoid Arrow issues
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        elif pd.api.types.is_integer_dtype(df_clean[col]):
            # Convert to nullable int
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce', downcast='integer')
    
    # Try to identify and convert datetime columns
    datetime_cols = []
    for col in df_clean.columns:
        if any(keyword in col.lower() for keyword in ['pickup', 'dropoff', 'date', 'time']):
            try:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                datetime_cols.append(col)
            except:
                pass
    
    # Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    removed_rows = initial_rows - len(df_clean)
    
    if removed_rows > 0:
        st.info(f"ℹ️ Menghapus {removed_rows:,} baris duplikat")
    
    # Final conversion to ensure Arrow compatibility
    df_clean = df_clean.copy()
    
    return df_clean


def get_sample_gdrive_url() -> str:
    """
    Returns a sample Google Drive URL for testing
    """
    return "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing"


@st.cache_data(ttl=3600)
def load_multiple_files_from_gdrive(folder_url: str, file_pattern: str = "*.parquet") -> Optional[pd.DataFrame]:
    """
    Load and combine multiple files from a Google Drive folder
    
    Args:
        folder_url: Google Drive folder URL
        file_pattern: Pattern to match files (e.g., "yellow_tripdata_2023-*.parquet")
        
    Returns:
        Combined DataFrame from all matching files, or None if failed
    """
    try:
        st.info("📂 Fitur multi-file loading dari folder Google Drive")
        st.warning("⚠️ **Note:** Untuk load multiple files, Anda perlu:")
        st.info("1. Download semua file yang ingin digabungkan")
        st.info("2. Upload satu per satu, atau")
        st.info("3. Gabungkan file terlebih dahulu sebelum upload")
        st.info("💡 **Alternatif:** Gunakan Google Colab untuk merge files, lalu upload hasil merge")
        
        # For now, we'll provide instructions for manual merging
        st.code("""
# Contoh code untuk merge di Google Colab:
import pandas as pd
import glob

# List all parquet files
files = glob.glob('yellow_tripdata_2023-*.parquet')

# Read and combine
dfs = []
for file in files:
    df = pd.read_parquet(file)
    dfs.append(df)

# Combine all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Save combined file
combined_df.to_parquet('yellow_tripdata_2023_full.parquet')
        """, language='python')
        
        return None
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None
