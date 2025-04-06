import pandas as pd

def applyMAStrategy(data: pd.DataFrame, shortWindow: int = 10, longWindow: int = 50) -> pd.DataFrame:
    """
    Applies a simple Moving Average Crossover strategy.

    Args:
        data (pd.DataFrame): The historical price data (must include 'Close' column).
        shortWindow (int): The period for the short-term moving average.
        longWindow (int): The period for the long-term moving average.

    Returns:
        pd.DataFrame: Original data with added columns for moving averages and signals.
    """

    # Make sure the close column is in the DataFrame
    if 'Close' not in data.columns:
        raise ValueError("DataFrame must contain a 'Close' column.")
    
    # Calculate short and long moving averages
    data['ShortMA'] = data['Close'].rolling(window=shortWindow).mean() # Short-term moving average (sets the .rolling(window) = to shortWindow (shortWindow = 10))
    data['LongMA'] = data['Close'].rolling(window=longWindow).mean() # Long-term moving average (sets the .rolling(window) = to longWindow (longWindow = 50))

    # Generate signals column
    """
    Signal column logic:
    1. If the short moving average crosses above the long moving average, it's a buy signal (1) "Bullish".
    2. If the short moving average crosses below the long moving average, it's a sell signal (-1) "Bearish".
    3. If there's no crossover, the signal remains neutral (0) "hold".
    """

    data['Signal'] = 0 # Default to no signal (0)

    # .loc = Locate by label or condition (in this case, the condition is the shortMA > longMA or shortMA < longMA)
    # Locate all rows where the condition is satisfied then set the signal to 1 (buy) or -1 (sell)
    data.loc[data["ShortMA"] > data["LongMA"], "Signal"] = 1 # Buy signal = find all where shortMA > longMA and set the signal to 1 (buy)
    data.loc[data["ShortMA"] < data["LongMA"], "Signal"] = -1 # Sell signal = find all where shortMA < longMA and set the signal to -1 (sell)

    # Create a "position" column to track the current position
    data["Position"] = data["Signal"].diff() # finds the difference between the current signal and the previous signal

    return data