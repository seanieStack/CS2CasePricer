# CSGO Case Value Calculator

This script calculates the total value of CSGO cases based on current market prices from CSFloat. Useful for cases inside storage containers.

## Features
- Fetches the latest market prices for specified CS cases from CSFloat.
- Calculates the total value based on the number of cases.

## Installation

1. Clone the repository:
   ```sh
    git clone https://github.com/seanieStack/CS2CasePricer.git
    cd csgo-case-value-calculator
   
    pip install -r requirements.txt

    cp .env.example .env
    # Edit the .env file to add your API key found here: https://csfloat.com/profile
   ```
   
2. Edit your case numbers in `cs_cases.json`
3. Run the script
   ```sh
       python src/main.py
   ```
