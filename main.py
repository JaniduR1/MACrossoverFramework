from src.dataLoader import downloadPriceData
from src.movingAverageStrategy import applyMAStrategy
from src.plotSignals import plotSignals



dataFrame = downloadPriceData("BTC-USD", start="2018-01-01", end="2025-04-01")

dataWithSignals = applyMAStrategy(dataFrame)

plotSignals(dataWithSignals)
print(dataWithSignals[["Close", "ShortMA", "LongMA", "Signal", "Position"]].tail(10))