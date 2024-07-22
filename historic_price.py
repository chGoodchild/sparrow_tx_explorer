import subprocess
import json

def get_historic_price_with_curl(start_date, end_date):
    curl_command = [
        "curl",
        f"https://api.coindesk.com/v1/bpi/historical/close.json?start={start_date}&end={end_date}"
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True)
    if result.returncode == 0:
        # The curl command succeeded, parse the JSON data
        try:
            response_data = json.loads(result.stdout)
            return response_data
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
    else:
        # Curl command failed
        print(f"curl command failed with return code {result.returncode}")
        print(f"Error output: {result.stderr}")

    return None

def main():
    start_date = '2023-02-28'
    end_date = '2023-02-28'

    data = get_historic_price_with_curl(start_date, end_date)
    if data:
        print(data)

if __name__ == "__main__":
    main()

