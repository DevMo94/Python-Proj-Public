import yfinance as yf
import pandas as pd
from tabulate import tabulate
import time
from datetime import datetime


def get_stock_data(ticker):
    try:
        data = yf.download(ticker, period="2d", progress=False)
        if data.empty or len(data) < 2:
            print(f"No data available for {ticker}.")
            return None
        current_day_close = data['Close'].iloc[-1].item()
        previous_day_close = data['Close'].iloc[-2].item()
        return current_day_close, previous_day_close
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def endtime():
    now = datetime.now()
    market_close_time = now.replace(hour=15, minute=30, second=0, microsecond=0).time()
    return now.time() < market_close_time


if __name__ == "__main__":

    # List of stock holdings
    holdings = [
        {"ticker": "<Enter your ticker ID>", "bought_price": <Price of the stock>, "quantity": <Stock quantity>}
    ]

while endtime():
    results = []

    for stock in holdings:
        ticker = stock["ticker"]
        bought_price = stock["bought_price"]
        quantity = stock["quantity"]

        stock_data = get_stock_data(ticker)

        if stock_data is not None:
            current_day_close, previous_day_close = stock_data
            price_change = current_day_close - bought_price
            invested = bought_price * quantity
            current_value = current_day_close * quantity
            profit_loss = current_value - invested

            results.append({
                "Ticker": ticker[:12],
                "Bought Price": bought_price,
                "Quantity": quantity,
                "Invested (₹)": invested,
                "Current Price": current_day_close,
                "Current Value (₹)": current_value,
                "P/L (₹)": profit_loss,
                "Price Change (₹)": price_change
            })
        else:
            print(f"Skipping {ticker} due to missing data.")

    if results:
        df = pd.DataFrame(results)
        print(
            f"\nStocks Data Summary: \nRunning at {datetime.now().strftime('%H:%M:%S')} IST")
        print("\nTotal Profit/Loss (₹):", round(df["P/L (₹)"].sum(), 2))
        print("\n")
        print(tabulate(df, headers='keys', tablefmt="grid",
              showindex=False, stralign='left', numalign='right'))
        time.sleep(30)
    else:
        print("\nNo data to display.")

print("Market closed or time exceeded 3:30 PM IST. The code will stop running now.")
