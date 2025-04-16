from src.dataLoader import downloadPriceData
from src.movingAverageStrategy import applyMAStrategy
from src.plotSignals import plotSignals
from src.backtestStrategy import backtestMAStrategy
from src.plotBacktest import plotBacktestStrategy
from src.evaluatePerformance import evaluatePerformance
from src.backtestWithRisk import backtestWithRiskControl
from src.createMLDataset import createMLDataset
from src.trainMLModel import trainAndEvaluateModel, plotConfusionMatrix




dataFrame = downloadPriceData("BTC-USD", start="2018-01-01", end="2025-04-01")

dataWithSignals = applyMAStrategy(dataFrame)

plotSignals(dataWithSignals)
# print(dataWithSignals[["Close", "ShortMA", "LongMA", "Signal", "Position"]].tail(10))

# backtestedData = backtestMAStrategy(dataWithSignals)
backtestedData = backtestWithRiskControl(dataWithSignals, stopLoss=0.5, takeProfit=0.01)
plotBacktestStrategy(backtestedData)

# print(backtestedData[["Close", "ShortMA", "LongMA", "Signal", "Position", "Holdings", "Cash", "Total", "Trade"]].tail(20))

# trades = backtestedData[backtestedData["Trade"] != 0].copy()
# print(trades)

# Results
performance = evaluatePerformance(backtestedData)
print("\nStrategy Performance Summary:")
for key, value in performance.items():
    print(f"{key}: {value}")


# Prepare ML dataset
X_train, X_test, y_train, y_test = createMLDataset(dataWithSignals)

# Train and evaluate model
model, mlMetrics, mlPredictions = trainAndEvaluateModel(X_train, X_test, y_train, y_test)
plotConfusionMatrix(y_test, mlPredictions)


# Results
print("\nML Model Performance (3-day Lookahead):")
for key, value in mlMetrics.items():
    print(f"{key}: {value}")



