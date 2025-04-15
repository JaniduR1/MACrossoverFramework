import pandas as pd


def evaluatePerformance(data, initialCapital=10000):
    """
    Evaluates performance of the backtested strategy.

    Args:
        data (pd.DataFrame): The backtested DataFrame (must include 'Total', 'Trade', 'Cash', 'Holdings', 'Close').
        initialCapital (float): Starting capital used in the backtest.

    Returns:
        dict: A dictionary with performance metrics.
    """

    results = {} # Create a dictionary to hold performance results

    # Calculate Total Return - To measure how much the portfolio grew in % from the starting capital
    finalValue = data["Total"].iloc[-1] # # Get the last value in the "Total" column (final portfolio value)
    results["Total Return (%)"] = ((finalValue - initialCapital) / initialCapital) * 100 # # Calculate percentage return from the initial capital to the final value


    # Count number of trades - To measure how many trades were executed during the backtest
    numTrades = data["Trade"].abs().sum() # .abs() makes -1 become 1 (to count both buys and sells), then sum it
    results["Number of Trades"] = int(numTrades) # # Save the total trade count as an integer

    # Measures what % of trades were profitable
    trades = data[data["Trade"] != 0].copy() # # Get only rows where trades occurred (1 = buy, -1 = sell)


    tradeResults = [] # Store each trade's profit/loss result
    inTrade = False # Tracks whether currently in a trade
    entryPrice = 0.0 # Remembers the price at which it was bought

    for i, row in trades.iterrows(): # Go through each trade row one by one
        if row["Trade"] == 1 and not inTrade:
            entryPrice = row["Close"] # Save the price bought at
            inTrade = True # Mark in a trade now


        elif row["Trade"] == -1 and inTrade:
            exitPrice = row["Close"] # Save the price sold at
            tradeResults.append(exitPrice - entryPrice) # Calculate P/L for the trade
            inTrade = False # Mark not in a trade anymore
    


    if tradeResults: # Only run this if at least one trade has been completed
        wins = [r for r in tradeResults if r > 0]  # Filter only the profitable trades
        winRate = (len(wins) / len(tradeResults)) * 100  # Percent of profitable trades
        results["Win Rate (%)"] = round(winRate, 2)  # Round it to 2 decimal places
    else:
        results["Win Rate (%)"] = "N/A"  # If no trades were made, mark as not available

    return results # Return the performance summary as a dictionary

