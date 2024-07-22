from Historic_Crypto import HistoricalData
import pandas as pd
from datetime import datetime, timedelta

def get_historic_price(transaction_datetime):
    # Convert the string to a datetime object
    dt_object = datetime.strptime(transaction_datetime, '%Y-%m-%d %H:%M:%S')
    
    # Format the datetime to fit the API requirement 'YYYY-MM-DD-HH-MM'
    start_datetime = dt_object.strftime('%Y-%m-%d-%H-%M')
    end_datetime = (dt_object + timedelta(minutes=1)).strftime('%Y-%m-%d-%H-%M')  # Adds a small buffer

    # Initialize HistoricalData with corrected parameters
    try:
        # Using a granularity of 60 seconds (1 minute)
        historical_data = HistoricalData('BTC-USD', 60, start_datetime, end_datetime).retrieve_data()
        return historical_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def main():
    # Example transaction datetime
    transaction_datetime = '2024-02-13 22:02:36'
    
    # Fetching historical data
    data = get_historic_price(transaction_datetime)
    if not data.empty:
        print("Retrieved Data:")
        print(data)
    else:
        print("No data retrieved or an error occurred.")

if __name__ == "__main__":
    main()
