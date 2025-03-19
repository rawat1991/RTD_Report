import pandas as pd
import os

DATA_FILE = "data/reports.csv"

def ensure_data_file():
    """Ensure the data directory and file exist"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=[
            "Date", "VariantName", "BatchCode", "TotalCase", 
            "LooseCans", "EmptyRejection", "EmptySample", "WIPCans",
            "FilledRejection", "BreakdownRejection", "ManpowerDentRejection",
            "HighPressureRejection", "WaterCanRejection", "MachineDentCans",
            "FadeCans", "UnprintedCans", "ScratchedCans", "LidRejection",
            "QASample", "QAOtherSample", "RejectShipper"
        ]).to_csv(DATA_FILE, index=False)

def save_data(data):
    """Save new data to CSV file"""
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)
    new_df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    new_df.to_csv(DATA_FILE, index=False)

def load_data():
    """Load data from CSV file"""
    ensure_data_file()
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=['Date'])
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        numeric_columns = [
            "TotalCase", "LooseCans", "EmptyRejection", 
            "EmptySample", "WIPCans", "FilledRejection", "BreakdownRejection",
            "ManpowerDentRejection", "HighPressureRejection", "WaterCanRejection",
            "MachineDentCans", "FadeCans", "UnprintedCans", "ScratchedCans",
            "LidRejection", "QASample", "QAOtherSample", "RejectShipper"
        ]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def search_data(df, start_date=None, end_date=None, batch_code=None, variant_name=None):
    """Search and filter data"""
    filtered_df = df.copy()

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date) & 
            (filtered_df["Date"] <= end_date)
        ]

    if batch_code:
        filtered_df = filtered_df[filtered_df["BatchCode"] == batch_code]

    if variant_name:
        filtered_df = filtered_df[filtered_df["VariantName"] == variant_name]

    return filtered_df

def delete_report(df, date=None, batch_code=None, variant_name=None, delete_all=False):
    """Delete reports based on filters or delete all"""
    if delete_all:
        df = pd.DataFrame(columns=df.columns)
    else:
        mask = pd.Series(True, index=df.index)
        if date is not None:
            mask &= (df["Date"] == date)
        if batch_code is not None:
            mask &= (df["BatchCode"] == batch_code)
        if variant_name is not None:
            mask &= (df["VariantName"] == variant_name)
        df = df[~mask]
    
    df.to_csv(DATA_FILE, index=False)
    return df