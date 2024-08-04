import json
from urllib.parse import quote, unquote
from requests import get
import concurrent.futures
import logging
from dotenv import dotenv_values

config = dotenv_values("../.env")
API_KEY = config.get("API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_cases(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def fetch_price(case, amount):
    try:
        response = get(f"https://csfloat.com/api/v1/listings?market_hash_name={case}&sort_by=lowest_price&limit=5",
                       headers={"Authorization": f"{API_KEY}"})

        if response.status_code != 200:
            logging.error(f"Failed to fetch data for {unquote(case)}: {response.status_code}")
            return 0

        json_data = response.json()

        if len(json_data) < 5:
            logging.warning(f"Not enough listings for {unquote(case)}")
            return 0

        price = json_data[4]["price"]
        price_string = f"{price / 100.0:.2f}"

        logging.info(f"{unquote(case)} * {amount} @ ${price_string}")
        return price * amount
    except Exception as e:
        logging.error(f"Error fetching price for {unquote(case)}: {str(e)}")
        return 0


def calculate_total_value(encoded_cases):
    value = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_case = {executor.submit(fetch_price, case, amount): (case, amount) for case, amount in
                          encoded_cases.items() if amount > 0}

        for future in concurrent.futures.as_completed(future_to_case):
            case, amount = future_to_case[future]
            try:
                value += future.result()
            except Exception as exc:
                logging.error(f"{unquote(case)} generated an exception: {exc}")

    logging.info(f"Total value: ${value / 100.0:.2f}")
    return value


def main():
    file_path = "../cs_cases.json"
    cases = load_cases(file_path)
    encoded_cases = {quote(key): value for key, value in cases.items()}
    calculate_total_value(encoded_cases)


if __name__ == "__main__":
    main()
