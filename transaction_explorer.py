from Historic_Crypto import HistoricalData
import pandas as pd
from datetime import datetime, timedelta

def fetch_bitcoin_price_at_transaction_minute(transaction_datetime):
    # Format the datetime to fit the API requirement 'YYYY-MM-DD-HH-MM'
    start_datetime = transaction_datetime.strftime('%Y-%m-%d-%H-%M')
    end_datetime = (transaction_datetime + timedelta(minutes=1)).strftime('%Y-%m-%d-%H-%M')  # Adding 1 minute to cover the exact minute of the transaction

    # Initialize HistoricalData with corrected parameters
    try:
        # Using a granularity of 60 seconds (1 minute)
        historical_data = HistoricalData('BTC-USD', 60, start_datetime, end_datetime).retrieve_data()
        if not historical_data.empty:
            # Extract the close price of the first retrieved minute
            close_price = historical_data['close'].iloc[0]  # 'close' of the first minute
            return close_price
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    file_path = '../transactions/transactions.csv'
    print("Reading data from file...")
    df = pd.read_csv(file_path)
    
    df['Date (UTC)'] = pd.to_datetime(df['Date (UTC)'], errors='coerce')
    if df['Date (UTC)'].isnull().any():
        print("Some dates couldn't be parsed and will be skipped.")
    
    df = df.dropna(subset=['Date (UTC)'])
    
    # Initialize a new column for USD values
    df['Value (USD)'] = None
    
    for index, row in df.iterrows():
        transaction_datetime = row['Date (UTC)']
        print(f"Fetching price for {transaction_datetime}")
        price = fetch_bitcoin_price_at_transaction_minute(transaction_datetime)
        if price is not None:
            df.at[index, 'Value (USD)'] = row['Value'] * price
            print(f"Fetched price ${price} for date {transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')} at index {index}")
        else:
            print(f"No price data available for {transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    df.to_csv('../transactions/updated_transactions.csv', index=False)
    print("Updated CSV file has been saved.")

if __name__ == "__main__":
    main()

