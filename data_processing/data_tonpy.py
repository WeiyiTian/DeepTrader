import os
import numpy as np
import pandas as pd

# Define paths
folder_path = "./HS300_csv"  # Change this to your actual folder
save_dir = "./HS300DS"  # Ensure this directory exists
npy_file_path = os.path.join(save_dir, "stocks_data.npy")

# Create the directory if it does not exist
os.makedirs(save_dir, exist_ok=True)

# Get list of Excel files
file_list = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Initialize list to store data
all_data = []

# Read each Excel file
for file in file_list:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path, engine='openpyxl')
    data_array = df.to_numpy()
    all_data.append(data_array)

# Convert to NumPy array
stocks_data = np.array(all_data, dtype=object)  # Use dtype=object for variable-sized arrays

# Save the file
np.save(npy_file_path, stocks_data)

print(f"Successfully saved: {npy_file_path}")
