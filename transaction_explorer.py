import subprocess
import json
import pandas as pd
from datetime import datetime

def fetch_bitcoin_price_with_curl(date):
    formatted_date = date.strftime('%Y-%m-%d')
    curl_command = [
        "curl",
        f"https://api.coindesk.com/v1/bpi/historical/close.json?start={formatted_date}&end={formatted_date}"
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            response_data = json.loads(result.stdout)
            price = response_data['bpi'].get(formatted_date)
            if price:
                print(f"Price on {formatted_date}: ${price}")
                return price
            else:
                print(f"Price data missing for {formatted_date}. Available data: {response_data['bpi']}")
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
    else:
        print(f"curl command failed with return code {result.returncode}")
        print(f"Error output: {result.stderr}")
    return None

def main():
    file_path = '../transactions/transactions.csv'
    print("Reading data from file...")
    df = pd.read_csv(file_path)
    
    df['Date (UTC)'] = pd.to_datetime(df['Date (UTC)'], errors='coerce')
    if df['Date (UTC)'].isnull().any():
        print("Some dates couldn't be parsed and will be skipped.")
    
    # Drop rows with NaT in 'Date (UTC)' after conversion
    df = df.dropna(subset=['Date (UTC)'])
    
    print("Populating USD values...")
    df['Value (USD)'] = df.apply(
        lambda row: row['Value'] * fetch_bitcoin_price_with_curl(row['Date (UTC)'])
        if pd.notnull(row['Date (UTC)']) else None, axis=1
    )
    
    df.to_csv('../transactions/updated_transactions.csv', index=False)
    print("Updated CSV file has been saved.")

if __name__ == "__main__":
    main()

