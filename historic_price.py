from Historic_Crypto import HistoricalData
import pandas as pd
from datetime import datetime, timedelta


def get_historic_price(transaction_datetime):
    # Convert the string to a datetime object
    dt_object = datetime.strptime(transaction_datetime, '%Y-%m-%d %H:%M:%S')
    
    # Format the datetime to fit the API requirement 'YYYY-MM-DD-HH-MM'
    start_datetime = dt_object.strftime('%Y-%m-%d-%H-%M')
    end_datetime = (dt_object + timedelta(minutes=1)).strftime('%Y-%m-%d-%H-%M')  # Adds a small buffer to ensure the minute is covered

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
    # Example transaction datetime
    transaction_datetime = '2024-02-13 22:02:36'
    
    # Fetching historical data
    close_price = get_historic_price(transaction_datetime)
    if close_price is not None:
        print(f"Retrieved Closing Price: ${close_price}")
    else:
        print("No data retrieved or an error occurred.")

if __name__ == "__main__":
    main()

