import os
from glob import glob
import pandas as pd

# Define the correct folder path
folder_path = "./HS300"  # Ensure this is correct
output_folder = "./HS300_csv"

# Get a sorted list of all .xlsx files in the folder
file_list = sorted(glob(os.path.join(folder_path, "*.xlsx")))

# Create a dictionary to store each stock's DataFrame separately
stock_data_dict = {}

# Expected columns for safety
expected_columns = [
    "日期", "开盘价(元)", "最高价(元)", "最低价(元)", "收盘价(元)",
    "涨跌幅", "成交额(百万)", "成交量"
]

# Process each file and store it separately in the dictionary
for stock_id, file_path in enumerate(file_list, start=1):
    df = pd.read_excel(file_path)

    # Ensure all expected columns exist
    df = df.reindex(columns=expected_columns, fill_value=pd.NA)

    # Convert date column to datetime format
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")  # Convert and handle errors

    # Rename columns to standardized format
    df = df.rename(columns={
        "日期": "Day",
        "开盘价(元)": "Opening",
        "最高价(元)": "Highest",
        "最低价(元)": "Lowest",
        "收盘价(元)": "Closing",
        "涨跌幅": "Changes",
        "成交额(百万)": "Amount",
        "成交量": "Volume"
    })

    # Store in dictionary with stock_id as the key
    df.index = df['Day']
    df = df.drop('Day',axis=1)
    stock_data_dict[stock_id] = df

    # output_csv_path = os.path.join(output_folder, f"stock_{stock_id}.csv")
    # df.to_csv(output_csv_path, index=True, encoding="utf-8-sig")

# Print a sample output to check
print(f"Loaded {len(stock_data_dict)} stock files.")
print(stock_data_dict[1].head())  # Show first stock's first rows
