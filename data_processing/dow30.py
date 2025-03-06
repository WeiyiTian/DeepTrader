import yfinance as yf
import pandas as pd
import os

# List of Dow Jones 30 tickers
dow_30_tickers = ["MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DOW",
                 "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
                  "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WMT", "WBA", "DIS", "^DJI"]

# Create a directory to store the files
output_dir = "data/DOW30/dow30_data"
os.makedirs(output_dir, exist_ok=True)

# Define the time period for the data (e.g., max history available)
period = "max"

# Download, clean, and save each stock separately
for ticker in dow_30_tickers:
    print(f"Downloading {ticker}...")
    stock_data = yf.download(ticker, period=period)
    
    if stock_data.empty:
        print(f"Warning: No data found for {ticker}!")
        continue

    # Forward fill NaN values
    stock_data.ffill(inplace=True)

    # Save to CSV file
    file_path = os.path.join(output_dir, f"{ticker}.csv")
    stock_data.to_csv(file_path)
    print(f"Saved {ticker} data to {file_path}")

print("Download completed!")