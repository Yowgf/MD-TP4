"""Implements methods to show the variance, kurtosis and skew of
the numerical part of the data.

Here we currently only consider the data from prices.csv.

"""

from scipy.stats import kurtosis, skew

def showVariance(pricesDf):
    numericalData = pricesDf.drop(["date", "symbol"], axis=1)

    print("Numerical data variance for prices.csv: ")
    print(numericalData.var())

def showKurtosis(pricesDf):
    numericalData = pricesDf.drop(["date", "symbol"], axis=1)
    
    print("Fisher kurtosis of the numerical data from prices.csv," +
          " by column:")
    print(list(numericalData.columns))
    print(kurtosis(numericalData, fisher=True))

def showSkew(pricesDf):
    numericalData = pricesDf.drop(["date", "symbol"], axis=1)
    
    print("Skew of the numerical data from prices.csv, by column:")
    print(list(numericalData.columns))
    print(skew(numericalData))
