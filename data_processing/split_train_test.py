import os
import pandas as pd
from glob import glob
import numpy as np

# Define paths
input_folder = "./HS300_csv"  # Folder containing stock CSV files
train_output_folder = "./HS300_train"
test_output_folder = "./HS300_test"
save_dir = "./HS300DS"  # Ensure this directory exists
npy_train_path = os.path.join(save_dir, "stocks_train_data.npy")
npy_test_path = os.path.join(save_dir, "stocks_test_data.npy")

# Create output directories if they don't exist
os.makedirs(train_output_folder, exist_ok=True)
os.makedirs(test_output_folder, exist_ok=True)

# Define strict date ranges for train and test splits
train_start, train_end = pd.Timestamp("2005-01-01"), pd.Timestamp("2012-12-31")
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
        train_df.to_csv(os.path.join(train_output_folder, f"{stock_name}_train.csv"), index=False, encoding="utf-8-sig")
        train_data_array = train_df.to_numpy()
        all_train_data .append(train_data_array)
    if df['Day'][0] <= test_start:
        test_df = df[(df["Day"] >= test_start) & (df["Day"] <= test_end)]
        test_df.to_csv(os.path.join(test_output_folder, f"{stock_name}_test.csv"), index=False, encoding="utf-8-sig")
        test_data_array = test_df.to_numpy()
        all_test_data.append(test_data_array)

    stocks_train_data = np.array(all_train_data, dtype=object)  # Use dtype=object for variable-sized arrays
    stocks_test_data = np.array(all_test_data, dtype=object) 

# Save the file
np.save(npy_train_path, stocks_train_data)
np.save(npy_test_path, stocks_test_data)

# print(f"Successfully saved: {npy_file_path}")


