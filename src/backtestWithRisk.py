import pandas as pd

def backtestWithRiskControl(data, initialCapital=10000, stopLoss=0.1, takeProfit=0.2):
    """
    Backtests the MA crossover strategy with stop loss and take profit logic.

    Args:
        data (pd.DataFrame): Strategy DataFrame with 'Close' and 'Position' columns.
        initialCapital (float): Starting cash.
        stopLoss (float): % drop from entry price to trigger stop loss (e.g. 0.1 = 10%)
        takeProfit (float): % rise from entry price to trigger take profit (e.g. 0.2 = 20%)

    Returns:
        pd.DataFrame: Data with updated cash, holdings, total value, and trades.
    """
    data = data.copy()

    # Fill missing values if needed
    data["Signal"] = data["Signal"].fillna(0)
    data["Position"] = data["Position"].fillna(0)

    # Portfolio state columns
    data["Holdings"] = 0.0
    data["Cash"] = float(initialCapital)
    data["Total"] = float(initialCapital)
    data["Trade"] = 0.0

    inPosition = False
    entryPrice = 0.0

    # Loop through each row in the DataFrame (one day at a time)
    for i in range(len(data)):
        row = data.iloc[i]  # Get the current row

        currentPrice = row["Close"]  # Price used for entry, stop loss, take profit

        # BUY Condition: If a buy signal appears and no active position exists
        if row["Position"] > 0 and not inPosition:
            entryPrice = currentPrice  # Save the entry price
            data.at[data.index[i], "Holdings"] = initialCapital  # Convert all cash to holdings
            data.at[data.index[i], "Cash"] = 0.0  # Cash is now fully used
            data.at[data.index[i], "Trade"] = 1  # Mark trade as Buy
            inPosition = True  # Flag that a position is now active

        # In a trade, check for stop loss or take profit conditions
        elif inPosition:
            # Calculate current value of asset held
            qty = initialCapital / entryPrice
            currentValue = qty * currentPrice
            data.at[data.index[i], "Holdings"] = currentValue  # Update holding value

            # Check for stop loss
            if currentPrice <= entryPrice * (1 - stopLoss):
                # Triggered stop loss condition
                data.at[data.index[i], "Cash"] = currentValue  # Sell the asset
                data.at[data.index[i], "Holdings"] = 0.0  # No longer holding
                data.at[data.index[i], "Trade"] = -1  # Mark this as a forced sell
                inPosition = False  # Exit position
                continue  # Skip the rest of this row

            # Check for take profit
            elif currentPrice >= entryPrice * (1 + takeProfit):
                # Triggered take profit condition
                data.at[data.index[i], "Cash"] = currentValue
                data.at[data.index[i], "Holdings"] = 0.0
                data.at[data.index[i], "Trade"] = -1
                inPosition = False
                continue

            # Signel based sell condition
            elif row["Position"] < 0:
                # If stop loss and take profit didn’t trigger, fall back to original sell signal
                data.at[data.index[i], "Cash"] = currentValue
                data.at[data.index[i], "Holdings"] = 0.0
                data.at[data.index[i], "Trade"] = -1
                inPosition = False

        # Portfoltio Update (every row)
        data.at[data.index[i], "Total"] = data.at[data.index[i], "Cash"] + data.at[data.index[i], "Holdings"]
    return data  # Return the full DataFrame with updated portfolio tracking and trade actions
