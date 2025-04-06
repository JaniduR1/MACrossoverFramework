# Download Historical Data from Yahoo Finance

import yfinance as yf
import pandas as pd
import os


def downloadPriceData(symbol: str, start: str, end: str, saveTo: str = "data/") -> pd.DataFrame:
    """
    Download historical price data from Yahoo Finance.

    Args:
        symbol (str): The stock symbol to download data for.
        start (str): The start date in 'YYYY-MM-DD' format.
        end (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A DataFrame containing the historical price data.
    """
    # Check if the data already exists
    filename = f"{saveTo}{symbol}_{start}_{end}.csv"

    # Try loading cached file first
    if os.path.exists(filename):
        print(f"Loading data from {filename}")
        try:
            df = pd.read_csv(filename, index_col=0, parse_dates=True)

            # Try converting 'Close' to numeric (this will fail if it's not a clean file)
            df["Close"] = pd.to_numeric(df["Close"])
            return df

        except Exception as e:
            print(f"Error reading cached file: {e}")
            print("Deleting corrupted file and redownloading...")
            os.remove(filename)

    # If no file or deleted bad file, download fresh data
    print(f"Downloading data for {symbol} from {start} to {end}")
    df = yf.download(symbol, start=start, end=end, auto_adjust=False)

    # Clean MultiIndex column names if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Save cleaned version
    os.makedirs(saveTo, exist_ok=True)
    df.to_csv(filename)

    return df