import matplotlib.pyplot as plt
import os

def plotSignals(data, symbol="BTC-USD", saveTo="images/"):
    """
    Plot closing price, moving averages, and buy/sell signals.

    Args:
        data (pd.DataFrame): DataFrame containing 'Close', 'ShortMA', 'LongMA', 'Signal', and 'Position' columns.
        symbol (str): Ticker symbol used in the plot title and filename.
        saveTo (str): Directory to save the image file.
    """

    # Create the images/ folder if it doesn't exist
    os.makedirs(saveTo, exist_ok=True)

    # Set the figure size
    plt.figure(figsize=(16, 8))


    # Plot the main price and moving averages
    plt.plot(data.index, data['Close'], label='Closing Price', linewidth=1.5)
    plt.plot(data.index, data['ShortMA'], label='Short Moving Average', linestyle="--")
    plt.plot(data.index, data['LongMA'], label='Long Moving Average', linestyle="--")


    # Plot buy signals (where Position == 1 or 2) 
    buySignels = data[data['Position'] > 0]
    plt.scatter(buySignels.index, buySignels['Close'], marker='^', color='green', label='Buy Signal', zorder=5)

    # Plot sell signals (where Position == -1 or -2)
    sellSignals = data[data['Position'] < 0]
    plt.scatter(sellSignals.index, sellSignals['Close'], marker='v', color='red', label='Sell Signal', zorder=5)

    # Set the title and labels
    plt.title(f'{symbol} Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)


    imagePath = f"{saveTo}{symbol}MASignals.png"
    plt.tight_layout()
    plt.savefig(imagePath)
    print(f"Plot saved to: {imagePath}")
    plt.close()
