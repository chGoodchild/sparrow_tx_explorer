import requests
import pandas as pd
from datetime import datetime

# Cache dictionary for prices
price_cache = {}

def fetch_bitcoin_price_original(date):
    # Basic fetch without caching or detailed debugging
    return fetch_bitcoin_price_debug(date)

def fetch_bitcoin_price_debug(date):
    # Detailed debugging information
    formatted_date = date.strftime('%Y-%m-%d')
    url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
    params = {'start': formatted_date, 'end': formatted_date}
    response = requests.get(url, params=params)
    
    print(f"Making API call to: {url} with params: start={formatted_date} & end={formatted_date}")
    print(f"Response Status Code: {response.status_code}")  # Log status code
    if response.status_code == 200:
        print("Response OK")
        price_data = response.json()
        print(f"API Response Data: {price_data}")  # Log raw API response data

        # Extracting price information
        if 'bpi' in price_data and formatted_date in price_data['bpi']:
            price = price_data['bpi'][formatted_date]
            print(f"Price on {formatted_date}: ${price}")
            return price
        else:
            # This checks for any available prices and reports on their dates
            available_dates = ", ".join(price_data['bpi'].keys()) if 'bpi' in price_data else "None"
            print(f"Price data missing for {formatted_date}. Available data dates: {available_dates}")
            return None
    else:
        print(f"Failed to fetch data for {formatted_date}: HTTP {response.status_code}")
        print(f"Response Text: {response.text}")  # Log error response
        return None


def fetch_bitcoin_price_cached(date):
    # Using caching to minimize API calls
    formatted_date = date.strftime('%Y-%m-%d')
    if formatted_date in price_cache:
        print(f"Using cached data for {formatted_date}")
        return price_cache[formatted_date]
    
    price = fetch_bitcoin_price_debug(date)
    price_cache[formatted_date] = price
    return price

def main():
    fetch_bitcoin_price = fetch_bitcoin_price_debug

    file_path = '../transactions/transactions.csv'
    print("Reading data from file...")
    df = pd.read_csv(file_path)
    
    df['Date (UTC)'] = pd.to_datetime(df['Date (UTC)'], errors='coerce')
    if df['Date (UTC)'].isnull().any():
        print("Some dates couldn't be parsed and will be skipped.")
    df = df.dropna(subset=['Date (UTC)'])
    
    print("Populating USD values...")
    df['Value (USD)'] = df.apply(
        lambda row: row['Value'] * fetch_bitcoin_price(row['Date (UTC)'])
        if pd.notnull(row['Date (UTC)']) and fetch_bitcoin_price(row['Date (UTC)']) is not None
        else None, axis=1
    )
    
    df.to_csv('../transactions/updated_transactions.csv', index=False)
    print("Updated CSV file has been saved.")

if __name__ == "__main__":
    main()

