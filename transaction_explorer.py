from Historic_Crypto import HistoricalData
import pandas as pd
from datetime import datetime, timedelta

def fetch_bitcoin_price_at_transaction_minute(transaction_datetime, currency_pair):
    # Adjust the currency pair based on the required output ('BTC-USD' for US dollars, 'BTC-EUR' for Euros)
    start_datetime = transaction_datetime.strftime('%Y-%m-%d-%H-%M')
    end_datetime = (transaction_datetime + timedelta(minutes=1)).strftime('%Y-%m-%d-%H-%M')

    # Initialize HistoricalData with corrected parameters
    try:
        historical_data = HistoricalData(currency_pair, 60, start_datetime, end_datetime).retrieve_data()
        if not historical_data.empty:
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

    # Initialize new columns for USD and EUR values and prices
    df['Value (USD)'] = None
    df['Price at Transaction (USD)'] = None
    df['Value (EUR)'] = None
    df['Price at Transaction (EUR)'] = None
    
    for index, row in df.iterrows():
        transaction_datetime = row['Date (UTC)']
        print(f"Fetching price for {transaction_datetime}")
        usd_price = fetch_bitcoin_price_at_transaction_minute(transaction_datetime, 'BTC-USD')
        eur_price = fetch_bitcoin_price_at_transaction_minute(transaction_datetime, 'BTC-EUR')
        
        if usd_price is not None:
            df.at[index, 'Price at Transaction (USD)'] = usd_price
            df.at[index, 'Value (USD)'] = row['Value'] * usd_price / 100000000
            print(f"Fetched USD price ${usd_price} for date {transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')} at index {index}")
        else:
            print(f"No USD price data available for {transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        if eur_price is not None:
            df.at[index, 'Price at Transaction (EUR)'] = eur_price
            df.at[index, 'Value (EUR)'] = row['Value'] * eur_price / 100000000
            print(f"Fetched EUR price €{eur_price} for date {transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')} at index {index}")
        else:
            print(f"No EUR price data available for {transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    df.to_csv('../transactions/updated_transactions.csv', index=False)
    print("Updated CSV file has been saved.")

if __name__ == "__main__":
    main()

