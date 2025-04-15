from src.dataLoader import downloadPriceData
from src.movingAverageStrategy import applyMAStrategy
from src.plotSignals import plotSignals
from src.backtestStrategy import backtestMAStrategy
from src.plotBacktest import plotBacktestStrategy
from src.evaluatePerformance import evaluatePerformance



dataFrame = downloadPriceData("BTC-USD", start="2018-01-01", end="2025-04-01")

dataWithSignals = applyMAStrategy(dataFrame)

plotSignals(dataWithSignals)
# print(dataWithSignals[["Close", "ShortMA", "LongMA", "Signal", "Position"]].tail(10))

backtestedData = backtestMAStrategy(dataWithSignals)
plotBacktestStrategy(backtestedData)

# print(backtestedData[["Close", "ShortMA", "LongMA", "Signal", "Position", "Holdings", "Cash", "Total", "Trade"]].tail(20))

# trades = backtestedData[backtestedData["Trade"] != 0].copy()
# print(trades)

performance = evaluatePerformance(backtestedData)
print("\nStrategy Performance Summary:")
for key, value in performance.items():
    print(f"{key}: {value}")

