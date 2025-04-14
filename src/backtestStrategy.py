import pandas as pd

def backtestMAStrategy(data, initialCapital=10000):
    """
    Simulates trades for a Moving Average Crossover strategy using 'Position' signals.

    Args:
        data (pd.DataFrame): Should include 'Close' and 'Position' columns.
        initialCapital (float): Starting money for the simulation.

    Returns:
        pd.DataFrame: Data with extra columns for cash, holdings, and portfolio value.
    """

    data = data.copy() # Create a separate copy of the original DataFrame to not modify the original data. Just need to work with a temporary version


    # Fill in missing (NaN) values just in case any are left (replaces any missing values with 0)
    # Ensures the strategy logic doesn’t break if a row is incomplete
    data['Signal'] = data["Signal"].fillna(0)
    data['Position'] = data['Position'].fillna(0)


    data['Holdings'] = 0.0 # Tracks how much value you have invested in Bitcoin at any time. Starts at 0 since nothing has been bought.
    data['Cash'] = float(initialCapital) # Tracks how much money is sitting as cash. Starts as initialCapital ($10,000) since its not in any trade yet.
    data['Total'] = float(initialCapital) # Combines both: Cash + Holdings. This is your account balance each day.
    data['Trade'] = 0.0 # Used to mark trades. Will mark 1 for buy, -1 for sell, 0 for no trade

    # Tracks if you're currently "in a trade" (i.e., holding Bitcoin) 
    inPosition = False # (False means: you're not currently holding any Bitcoin It becomes True once you buy in (enter a position))
    
    entryPrice = 0.0 # Will remember the price at which you bought

    for i in range(len(data)): # Go row by row through the DataFrame (e.g. 2000 days of price history)
        row = data.iloc[i] # Get the row at position i, row is now a single row of the table "Series". Returns the entire row, not just one value

        # BUY condition
        if row['Position'] > 0 and not inPosition: # If a buy signal is detected (Position > 0) AND you're not already in a trade (not inPosition)
            entryPrice = row['Close'] # Remember the price at which you bought
            data.at[data.index[i], "Holdings"] = initialCapital # Buy full with all cash
            data.at[data.index[i], "Cash"] = 0.0 # No cash left after buying
            data.at[data.index[i], "Trade"] = 1 # Mark this row as a buy trade
            inPosition = True # Now you're in a trade

        # SELL condition
        elif row['Position'] < 0 and inPosition: # If a sell signal is detected (Position < 0) AND you're currently in a trade (inPosition)
            exitPrice = row['Close'] # Remember the price at which you sold
            qty = initialCapital / entryPrice # Calculate how much you bought (if you had $10,000 and BTC was $20,000, you bought 0.5 BTC)
            proceeds = qty * exitPrice # Calculate how much you made from selling 
            data.at[data.index[i], "Cash"] = proceeds # Put the money from selling back into cash (Update Cash Value)
            data.at[data.index[i], "Holdings"] = 0 # No more holdings after selling
            data.at[data.index[i], "Trade"] = -1 # Mark this row as a sell trade
            inPosition = False # Now you're not in a trade anymore
        
        # Hold position
        elif inPosition: # If you're in a trade but no buy/sell signal is detected
            qty = initialCapital / entryPrice # Calculate how much you bought (if you had $10,000 and BTC was $20,000, you bought 0.5 BTC)
            data.at[data.index[i], "Holdings"] = qty * row["Close"] # Update the value of your holdings based on the current price

        # Update total
        data.at[data.index[i], "Total"] = data.at[data.index[i], "Cash"] + data.at[data.index[i], "Holdings"] # Update the total value of your account (cash + holdings)

    return data # Return the DataFrame with all the new columns added