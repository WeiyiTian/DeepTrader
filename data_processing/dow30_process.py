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

    # Rename columns to standardized format
    # df = df.rename(columns={
    #     "日期": "Day",
    #     "开盘价(元)": "Opening",
    #     "最高价(元)": "Highest",
    #     "最低价(元)": "Lowest",
    #     "收盘价(元)": "Closing",
    #     "涨跌幅": "Changes",
    #     "成交额(百万)": "Amount",
    #     "成交量(股)": "Volume"
    # })

    # Store in dictionary with stock_id as the key
    df.index = df['Day']
    df = df.drop('Day',axis=1)
    stock_data_dict[ticker] = df

    output_csv_path = os.path.join(output_folder, f"{ticker}.csv")
    df.to_csv(output_csv_path, index=True, encoding="utf-8-sig")



# Define paths
input_folder = "./data/DOW30/dow30_csv"  # Folder containing stock CSV files
train_output_folder = "./data/DOW30/dow30_train"
test_output_folder = "./data/DOW30/dow30_test"
save_dir = "./data/DOW30/dow30_ds"  # Ensure this directory exists
npy_train_path = os.path.join(save_dir, "dow_train_data.npy")
npy_test_path = os.path.join(save_dir, "dow_test_data.npy")

# Create output directories if they don't exist
os.makedirs(train_output_folder, exist_ok=True)
os.makedirs(test_output_folder, exist_ok=True)

# Define strict date ranges for train and test splits
train_start, train_end = pd.Timestamp("1992-01-02"), pd.Timestamp("2012-12-31")
test_start, test_end = pd.Timestamp("2013-01-01"), pd.Timestamp("2019-12-31")

# Get all CSV files in the folder
file_list = sorted(glob(os.path.join(input_folder, "*.csv")))
all_train_data = []
all_test_data = []


for file_path in file_list:
    # Load the CSV file
    df = pd.read_csv(file_path)
    # print(file_path)

    # Ensure "day" column is in datetime format
    df["Day"] = pd.to_datetime(df["Day"], errors="coerce")

    # Ensure data is sorted by date
    df = df.sort_values("Day")

    # Get train and test period data
    stock_name = os.path.basename(file_path).replace(".csv", "")
    
    if df['Day'][0] <= train_start:
        train_df = df[(df["Day"] >= train_start) & (df["Day"] <= train_end)]


        invalid_entries = train_df['Volume'].map(lambda x: x == 0.0).sum().sum()
        if invalid_entries > 190:
            print(f"Found {invalid_entries} invalid values (0.0 volume) in {file_path} training.")
            continue

        train_df.iloc[:, -2:] = (
                                train_df.iloc[:, -2:]
                                .replace(0.0, pd.NA)  # Replace 0.0 with NA to avoid filling unwanted zeros
                                .apply(pd.to_numeric, errors='coerce') 
                                .ffill()  # Forward fill
                                .infer_objects(copy=False)  # Ensure correct dtype inference
                            )

        train_df.to_csv(os.path.join(train_output_folder, f"{stock_name}_train.csv"), index=False, encoding="utf-8-sig")
        # train_data_array = train_df.to_numpy()
        train_data_array = train_df.drop("Day", axis = 1).to_numpy()

        all_train_data .append(train_data_array)

    if df['Day'][0] <= test_start:
        test_df = df[(df["Day"] >= test_start) & (df["Day"] <= test_end)]

        invalid_entries = test_df['Volume'].map(lambda x: x == 0.0).sum().sum()
        if invalid_entries > 170:
            print(f"Found {invalid_entries} invalid values (0.0 volume) in {file_path} testing.")
            continue

        test_df.iloc[:, -2:] = (
                                test_df.iloc[:, -2:]
                                .replace(0.0, pd.NA)  # Replace 0.0 with NA to avoid filling unwanted zeros
                                .apply(pd.to_numeric, errors='coerce') 
                                .ffill()  # Forward fill
                                .infer_objects(copy=False)  # Ensure correct dtype inference
                            )
        test_df.to_csv(os.path.join(test_output_folder, f"{stock_name}_test.csv"), index=False, encoding="utf-8-sig")
        # test_data_array = test_df.to_numpy()
        test_data_array = test_df.drop("Day", axis = 1).to_numpy()

        all_test_data.append(test_data_array)

stocks_train_data = np.array(all_train_data, dtype=object)  # Use dtype=object for variable-sized arrays
stocks_test_data = np.array(all_test_data, dtype=object) 

print(stocks_train_data.shape)
print(stocks_test_data.shape)

# Save the file
np.save(npy_train_path, stocks_train_data)
np.save(npy_test_path, stocks_test_data)

# print(f"Successfully saved: {npy_file_path}")


