import yfinance
import pandas as pd

def save_csv(data, dest=None):

    df = pd.DataFrame(data)

    df.to_csv(f"./{dest}.csv")


def get_ticker(ticker: str, star_date: str, end_date: str):

    hist = yfinance.Ticker(ticker).history(
        period="1d",
        interval="1h",
        start=star_date,
        end=end_date,
        prepost=True
    )

    save_csv(hist, ticker)

    return hist

hist = get_ticker("AAPL", '2024-01-05', '2024-01-10')