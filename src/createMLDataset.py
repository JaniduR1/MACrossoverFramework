import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

def createMLDataset(data, lookahead=3, testSize=0.2, randomState=42):
    """
    Prepares features and labels for ML using a lookahead price direction label and applies SMOTE.

    Args:
        data (pd.DataFrame): Must include a 'Close' column.
        lookahead (int): Number of days to look ahead when generating the label.
        testSize (float): Proportion of data to reserve for testing.
        randomState (int): For reproducibility.

    Returns:
        X_train, X_test, y_train, y_test: Balanced training sets and untouched test sets
    """
    df = data.copy()

    # Create features and labels
    # 1 if future price is higher than current price N days ahead, else 0
    df["Label"] = (df["Close"].shift(-lookahead) > df["Close"]).astype(int)

    # Drop rows with missing lookahead targets
    df = df.dropna()

    df["Return_1D"] = df["Close"].pct_change()                   # Daily return
    df["MA_5"] = df["Close"].rolling(window=5).mean()            # 5-day moving average
    df["MA_10"] = df["Close"].rolling(window=10).mean()          # 10-day moving average
    df["Volatility_5D"] = df["Close"].rolling(window=5).std()    # 5-day rolling std deviation (volatility)
    df["Volume_Change"] = df["Volume"].pct_change()              # Volume change as signal

    # Drop initial rows with NaNs from rolling functions
    df = df.dropna()

        # Define input features and target label
    featureCols = ["Return_1D", "MA_5", "MA_10", "Volatility_5D", "Volume_Change"]
    X = df[featureCols]
    y = df["Label"]

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=testSize, random_state=randomState, shuffle=False
    )

    # Apply SMOTE only on training data
    smote = SMOTE(random_state=randomState)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    return X_train_resampled, X_test, y_train_resampled, y_test
