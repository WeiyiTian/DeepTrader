import os
import pandas as pd
from glob import glob
import numpy as np

# Define paths
input_folder = "./data/HS300/market"  # Folder containing stock CSV files

save_dir = "./data/HS300/HS300DS"  # Ensure this directory exists
npy_path = os.path.join(save_dir, "market_data.npy")

start = pd.Timestamp("2005-01-01")
end = pd.Timestamp("2019-12-31")
all_data = []

file_list = sorted(glob(os.path.join(input_folder, "*.csv")))

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
    
    if df['Day'][0] <= start:
        train_df = df[(df["Day"] >= start) & (df["Day"] <= end)]


        invalid_entries = train_df['Volume'].map(lambda x: x == 0.0).sum().sum()
        if invalid_entries > 300:
            #print(f"Found {invalid_entries} invalid values (0.0 volume) in {file_path} training.")
            continue

        train_df.iloc[:, -2:] = (
                                train_df.iloc[:, -2:]
                                .replace(0.0, pd.NA)  # Replace 0.0 with NA to avoid filling unwanted zeros
                                .apply(pd.to_numeric, errors='coerce') 
                                .ffill()  # Forward fill
                                .infer_objects(copy=False))  # Ensure correct dtype inferenc)


        data_array = train_df.drop("Day", axis = 1).to_numpy()

        all_data.append(data_array)


stocks_data = np.array(all_data, dtype=object)  # Use dtype=object for variable-sized arrays

print(stocks_data.shape)

stocks_data  = stocks_data.reshape(stocks_data.shape[1], stocks_data.shape[2])
print(stocks_data.shape)

# Save the file
np.save(npy_path, stocks_data)

