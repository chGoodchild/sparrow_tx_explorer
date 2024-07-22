from Historic_Crypto import HistoricalData
import pandas as pd

def get_historic_price(start_date, end_date):
    # Adjust end_date to include the time for the end of the day to ensure coverage of the entire day
    start_datetime = f"{start_date}-00-00"  # Start at the beginning of the day
    end_datetime = f"{end_date}-23-59"      # End at the last minute of the day

    # Initialize HistoricalData with corrected parameters
    try:
        # The granularity is set to 86400 seconds (1 day)
        historical_data = HistoricalData('BTC-USD', 86400, start_datetime, end_datetime).retrieve_data()
        return historical_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def main():
    start_date = '2023-02-28'
    end_date = '2023-02-28'
    
    # Fetching historical data
    data = get_historic_price(start_date, end_date)
    if not data.empty:
        print("Retrieved Data:")
        print(data)
    else:
        print("No data retrieved or an error occurred.")

if __name__ == "__main__":
    main()

