# Moving Average Crossover Trading Strategy

This project implements a fully automated and modular trading strategy based on the Moving Average (MA) Crossover technique. The goal is to create a data-driven trading framework that:

- Uses historical market data to detect trade signals based on moving average crossovers
- Supports backtesting, evaluation, and parameter tuning
- Can be converted into a REST API for integration with other systems
- Will be prepared for real-money trading via a broker API (e.g., Alpaca)
- Includes the potential for future expansion with machine learning, risk management, and sentiment-based filters

The project is designed with clarity, modularity, and extensibility in mind. Each component is structured to support learning, experimentation, and real-world application.

#### Features

| Feature               | Description                                                                            |
|-----------------------|----------------------------------------------------------------------------------------|
| Data Loader        | Downloads historical price data and caches it locally                                 |
| Strategy Logic     | Implements the core logic to detect buy/sell signals using short and long moving averages |
| Backtesting Engine | To be added: Simulates trades on historical data with performance metrics             |
| API-Ready          | To be converted into a REST API after core system is stable                           |
| Streamlit UI       | Planned for visual testing and sharing on GitHub/Streamlit Cloud                      |

---

## Moving Average Strategy `movingAverageStrategy.py`

#### Moving Averages

A moving average (MA) smooths out price data to identify trends. This strategy uses:

- **Short-term MA** (e.g., 10-day): reacts quickly
- **Long-term MA** (e.g., 50-day): reacts slowly

The crossovers between these two moving averages generate trading signals.

#### Buy/Sell Signal Logic

| Logic                         | Description                               |
|------------------------------|-------------------------------------------|
| `shortMA > longMA`           | Signal = 1 (buy zone)                     |
| `shortMA < longMA`           | Signal = -1 (sell zone)                   |
| `shortMA == longMA`          | Signal = 0 (neutral/unknown)              |

These are calculated using `.rolling().mean()` for both short and long windows.

#### How `.loc[]` Is Used to Generate Signals

The `.loc[]` method in pandas is used to **locate and update rows in a DataFrame based on a condition**.

```python
data.loc[data["shortMA"] > data["longMA"], "signal"] = 1
data.loc[data["shortMA"] < data["longMA"], "signal"] = -1
```

**How it works:**

| Component | Explanation |
|-----------|-------------|
| `data.loc[...]`         | Accesses specific rows and columns in the DataFrame |
| `data["shortMA"] > data["longMA"]` | A condition that returns `True` for rows where shortMA is greater than longMA |
| `"signal"`              | The column to update |
| `= 1 / -1`              | The value to assign if the condition is met |

**Visual Breakdown**

| Row | shortMA | longMA | Condition (`shortMA > longMA`) | Action |
|-----|---------|--------|----------------------------------|--------|
| 0   | 50      | 55     | False                           | No update  
| 1   | 56      | 55     | True                            | Set signal = 1 (Buy)  
| 2   | 54      | 55     | False                           | No update  
| 3   | 60      | 58     | True                            | Set signal = 1 (Buy)  
| 4   | 57      | 57     | False                           | No update  

#### Detecting Crossover Events with `.diff()` and the `"position"` Column

After signals are generated, the `.diff()` method is used to track **when the signal changes** — this is crucial for detecting **crossover moments**.

```python
data["position"] = data["signal"].diff()
```

**What `.diff()` does:**

- `.diff()` subtracts the **previous row’s value** from the current row
- This helps detect when the signal **changes from one value to another**

**Example Output**

| Row | signal | position (`.diff()`) | What it means      |
|-----|--------|----------------------|---------------------|
| 0   | 0      | NaN                  | No previous row  
| 1   | 1      | 1                    | First bullish signal → Buy  
| 2   | 1      | 0                    | Still bullish → Hold  
| 3   | -1     | -2                   | First bearish signal → Sell  
| 4   | -1     | 0                    | Still bearish → Hold  


**Explanation in Plain English**

The `position` column shows the exact moment when the trend **changes**.  
This helps the system **enter or exit trades only once per crossover**, instead of repeating trades unnecessarily.


#### Why This Matters

Using `position` ensures:
- Trades only happen at **signal transition points**
- No duplicate or premature entries/exits occur
- You can **plot crossover arrows or labels** cleanly on a chart
- Backtesting logic becomes cleaner and more realistic

---

## Visualizing the Strategy: `plotSignals.py`

Describes how signals are visualized, how the graphs and plots are saved, and what the chart includes.

*Images created with matplotlib. Stored in `images/`*

---

## Backtesting Strategy Performance: `backtestStrategy.py`

A backtesting module simulates how the strategy would have performed using historical data. It tracks trades, portfolio value, and capital allocation over time.

### What is Backtesting?

Backtesting allows the strategy to be tested on past data using defined logic and conditions. This helps evaluate:

- Whether the signals would have been profitable
- How the portfolio would have grown or lost money
- When trades occurred and what actions were taken

### Logic Used

| Component     | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `Cash`        | Remaining uninvested capital                                                |
| `Holdings`    | Value of Bitcoin held (if a trade is open)                                  |
| `Total`       | Combined value of cash + holdings                                           |
| `Trade`       | 1 for Buy, -1 for Sell, 0 for no trade                                       |
| `inPosition`  | Tracks whether the system is currently in a trade (holding Bitcoin or not)  |
| `entryPrice`  | Tracks price at time of entry for return calculation                        |

The system executes trades when `Position` changes:

- `Position > 0`: Enter a trade (buy Bitcoin using all capital)
- `Position == -2`: Exit the trade (sell Bitcoin, move fully back to cash)

### Portfolio Equity Curve: `plotBacktest.py`

A visualization of the strategy’s overall portfolio value across time. This reflects **when the strategy was in/out of the market**, how long it held assets, and how well the value grew over time.

#### What it shows

- X-axis: Dates (timeline)
- Y-axis: Total portfolio value ($)
- Line: Cumulative equity curve from all trades

#### Output

- Image is saved automatically to: `images/portfolioEquityCurve.png`
- Useful to visually identify:
  - Periods of active trading
  - Capital growth phases
  - Drawdowns or missed opportunities

---

#### Sample Plot

A typical equity curve may include flat periods (not in a trade) and spikes (in a profitable trade). This helps evaluate strategy effectiveness without needing to inspect each trade manually.

```
Portfolio equity curve saved to: images/portfolioEquityCurve.png
```

---