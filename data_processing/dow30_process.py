import os
import pandas as pd
from glob import glob
import numpy as np

# Define the correct folder path
folder_path = "./data/DOW30/dow30_data"  # Ensure this is correct
output_folder = "./data/DOW30/dow30_csv"

print("Folder exists:", os.path.exists(output_folder))

# Get a sorted list of all .xlsx files in the folder
file_list = sorted(glob(os.path.join(folder_path, "*.csv")))

# Create a dictionary to store each stock's DataFrame separately
stock_data_dict = {}

# Expected columns for safety
# expected_columns = [
#     "日期", "开盘价(元)", "最高价(元)", "最低价(元)", "收盘价(元)",
#     "涨跌幅", "成交额(百万)", "成交量(股)"
# ]
expected_columns = [
    "Day", "Close", "High", "Low", "Open", "Volume"
]

# Process each file and store it separately in the dictionary
for stock_id, file_path in enumerate(file_list, start=1):
    print(file_path)
    df = pd.read_csv(file_path,skiprows=2)
    file_name = os.path.basename(file_path)  # "000001.SZ"
    ticker = os.path.splitext(file_name)[0]
    print(ticker)

    # Ensure all expected columns exist
    df.columns = expected_columns

    # Convert date column to datetime format
    df["Day"] = pd.to_datetime(df["Day"], errors="coerce")  # Convert and handle errors



    # Store in dictionary with stock_id as the key
    df.index = df['Day']
    df = df.drop('Day',axis=1)
    stock_data_dict[ticker] = df

    output_csv_path = os.path.join(output_folder, f"{ticker}.csv")
    df.to_csv(output_csv_path, index=True, encoding="utf-8-sig")
