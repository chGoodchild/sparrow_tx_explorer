import requests
import pandas as pd
from datetime import datetime

def fetch_bitcoin_price(date):
    # Convert date to the required format 'yyyy-mm-dd'
    formatted_date = date.strftime('%Y-%m-%d')
    url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
    params = {'start': formatted_date, 'end': formatted_date}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        price_data = response.json()
        # Accessing the price in USD for the given date
        price = price_data['bpi'][formatted_date] if formatted_date in price_data['bpi'] else None
        if price is not None:
            print(f"Price on {formatted_date}: ${price}")
        else:
            print(f"Price data missing for {formatted_date}")
        return price
    elif response.status_code == 404:
        print(f"No data available for date {formatted_date}")
        return None
    else:
        print(f"Failed to fetch data for date {formatted_date}: HTTP {response.status_code}")
        return None

def main():
    # Read data from the CSV file
    file_path = '../transactions/transactions.csv'
    print("Reading data from file...")
    df = pd.read_csv(file_path)
    
    # Attempt to convert the 'Date (UTC)' column to datetime, coercing errors
    df['Date (UTC)'] = pd.to_datetime(df['Date (UTC)'], errors='coerce')
    print("Processing date conversions...")
    
    # Filter out rows where the date conversion failed (i.e., 'Date (UTC)' is NaT)
    if df['Date (UTC)'].isnull().any():
        print("Some dates couldn't be parsed and will be skipped.")
    df = df.dropna(subset=['Date (UTC)'])
    
    print("Populating USD values...")
    # Populate the 'Value (USD)' column
    df['Value (USD)'] = df.apply(lambda row: row['Value'] * fetch_bitcoin_price(row['Date (UTC)']) if pd.notnull(row['Date (UTC)']) and fetch_bitcoin_price(row['Date (UTC)']) is not None else None, axis=1)
    
    # Save the updated dataframe to a new CSV file
    df.to_csv('../transactions/transactions.csv', index=False)
    print("Updated CSV file has been saved.")

if __name__ == "__main__":
    main()

