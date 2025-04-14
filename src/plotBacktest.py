import matplotlib.pyplot as plt
import os

def plotBacktestStrategy(data, saveTo="images/"):

    """
    Plot the portfolio's total value (equity curve) over time.

    Args:
        data (pd.DataFrame): DataFrame that contains a 'Total' column, representing portfolio value at each time step.
        saveTo (str): Folder path to save the output chart. Defaults to "images/".
    """
    
    
    # Create the images/ folder if it doesn't exist
    os.makedirs(saveTo, exist_ok=True)

    # Set the figure size
    plt.figure(figsize=(16, 8))

    plt.plot(data.index, data["Total"], label="Portfolio Value", linewidth=2)
    plt.title("Portfolio Equity Curve Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True)
    plt.legend()

    # Save
    imagePath = os.path.join(saveTo, "portfolioEquityCurve.png")
    plt.tight_layout()
    plt.savefig(imagePath)
    print(f"Portfolio equity curve saved to: {imagePath}")
    plt.close()