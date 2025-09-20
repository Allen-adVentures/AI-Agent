import pandas as pd
import glob
from datetime import datetime
from pathlib import Path
from typing import Tuple, List
from pydantic import BaseModel

class HourlyIntervalUsage(BaseModel):
    start_ts: datetime
    end_ts: datetime
    usage_kwh: float
    cost: float

class UsageBill(BaseModel):
    start_date: datetime
    end_date: datetime
    total_usage_kwh: float
    cost: float

def get_interval_df(data_dir: str = "data/billing_data") -> pd.DataFrame:
    """Load and combine all interval data CSV files."""
    data_dir = Path(data_dir)
    csv_files = sorted(list(data_dir.glob("*.csv")))
    
    if not csv_files:
        raise FileNotFoundError(f"No interval data files found in {data_dir}")
    
    # Read and combine all interval data files
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            # Add filename for debugging
            df['source_file'] = file.name
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if not dfs:
        raise ValueError("No valid interval data files could be read")
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Clean and transform data
    if "USAGE (kWh)" in combined_df.columns:
        combined_df["USAGE (kWh)"] = combined_df["USAGE (kWh)"].astype(str).str.replace(",", "").astype(float)
    if "COST" in combined_df.columns:
        combined_df["COST"] = combined_df["COST"].astype(str).str.replace(r'[\$,\s]', '', regex=True).astype(float)
    if all(col in combined_df.columns for col in ["DATE", "START TIME"]):
        combined_df["START DATETIME"] = pd.to_datetime(
            combined_df["DATE"] + ' ' + combined_df["START TIME"], 
            format="%m/%d/%y %H:%M", 
            errors='coerce'
        )
    if all(col in combined_df.columns for col in ["DATE", "END TIME"]):
        combined_df["END DATETIME"] = pd.to_datetime(
            combined_df["DATE"] + ' ' + combined_df["END TIME"], 
            format="%m/%d/%y %H:%M", 
            errors='coerce'
        )
    
    return combined_df

def get_bill_df(data_dir: str = "data/interval_data") -> pd.DataFrame:
    """Load and process billing data."""
    data_dir = Path(data_dir)
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No billing data files found in {data_dir}")
    
    # Read the billing data file
    try:
        df = pd.read_csv(csv_files[0])
        # Add filename for debugging
        df['source_file'] = csv_files[0].name
    except Exception as e:
        raise ValueError(f"Error reading billing data: {e}")
    
    # Clean and transform data
    if "START DATE" in df.columns:
        df["START DATE"] = pd.to_datetime(df["START DATE"], format="%m/%d/%y", errors="coerce")
    if "END DATE" in df.columns:
        df["END DATE"] = pd.to_datetime(df["END DATE"], format="%m/%d/%y", errors="coerce")
    if "USAGE (kWh)" in df.columns:
        df["USAGE (kWh)"] = df["USAGE (kWh)"].astype(str).str.replace(",", "").astype(float)
    if "COST" in df.columns:
        df["COST"] = df["COST"].astype(str).str.replace(r'[\$,\s]', '', regex=True).astype(float)
    
    return df
