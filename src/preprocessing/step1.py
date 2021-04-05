"""Step 1 for phase 2 of the MD-TP4 project.

"""

from numpy import log
from sklearn.model_selection import train_test_split

# Get value from other libraries
from ..loading import pricesDf, load_all, allLoadPreprocess
allLoadPreprocess()

def subsOpenClose(pricesDf):
    # Substitute "open" and "close" with
    # the mean       -- (open + close) / 2
    # the difference -- (open - close)
    # Create means column
    openCloseMean = (pricesDf["open"] + pricesDf["close"]) / 2
    # Create difference column
    openCloseDiff = pricesDf["close"] - pricesDf["open"]

    # Insert them in the dataset at the second position
    #   (just after the symbol column)
    pricesDf.insert(2, "ocMean", openCloseMean)
    pricesDf.insert(3, "ocDiff", openCloseDiff)
    pricesDf.drop("open", axis=1, inplace=True)
    pricesDf.drop("close", axis=1, inplace=True)

def loadFundDf():
    fundDf = load_all(["fundamentals"])
    fundDf.drop(fundDf.columns[0], axis=1, inplace=True)
    return fundDf

def buildDictFromTwoArrs(keyArr, valArr):
    newDict = {}
    for (key, val) in zip(keyArr, valArr):
        newDict[key] = val
    
    return newDict

"""Cut the rows in pricesDf whose companies are not mentioned in the
file "fundamentals.csv". This effectively introduced a loss of about
10% o them, but it doesn't seem to have done big damage to the final
model.

@see loadFundDf
@see buildDictFromTwoArrs

"""
def restrictToFundDf(pricesDf):
    fundDf = loadFundDf()

    subsOpenClose(pricesDf)
    originalSyms = pricesDf.symbol.unique()
    totAssetsBySym = fundDf.groupby(by="Ticker Symbol").mean()["Total Assets"]
    # Make sure that only symbols that were there at first are considered.
    # A weird thing is that the company Under Armor (UA) was in
    #   fundamentals.csv, but not in prices.csv.
    totAssetsSymList = [sym for sym in totAssetsBySym.index if sym in originalSyms]

    # Only consider companies for which we have an instance in the
    #   file fundamentals.csv. With this change, we go from 501 companies
    #   to 447 companies, in the dataset.
    filtPricesDf = pricesDf[pricesDf.apply(lambda row: row["symbol"] in totAssetsSymList, axis=1)]

    return filtPricesDf, totAssetsSymList, totAssetsBySym

"""Get the total assets values for each company from the file
"fundamentals.csv", and then substitute the symbols in pricesDf by
these.

"""
def symbolToAssets(pricesDf):
    filtPricesDf, totAssetsSymList, totAssetsBySym = restrictToFundDf(pricesDf)
    totAssetsDict = buildDictFromTwoArrs(totAssetsSymList, totAssetsBySym)
                                    
    # new column
    totAssetsCol = filtPricesDf["symbol"].replace(to_replace=totAssetsDict).copy()
    # Insert the new column and drop the old one
    filtPricesDf.insert(1, "totAssets", log(totAssetsCol))
    filtPricesDf.drop("symbol", axis=1, inplace=True)

    return filtPricesDf

# Normalize the dataset by z score (assumes gaussian distribution)
def z_normalize(df):
    mu = df.mean()
    sigma = df.std()
    return (df - mu) / sigma
    
def fetchFiltPricesDf(pricesDf):
    filtPricesDf = symbolToAssets(pricesDf)

    # Substitute volume column by its logarithm (note the + 1 needed)
    filtPricesDf = filtPricesDf.assign(volume=lambda df: log(df["volume"]+1))
    
    # Make date the index of the dataframe
    # The main issue is that I don't want the model to think
    #   that there is distance between points just because of
    #   the date.
    filtPricesDf = filtPricesDf.set_index("date")

    filtPricesDf = z_normalize(filtPricesDf)

    return filtPricesDf

def splitTrainTest(filtPricesDf, foldNum = 10):
    X = filtPricesDf.drop("ocMean", axis=1)
    y = filtPricesDf["ocMean"]

    return train_test_split(X, y, test_size=1 / foldNum)

def printCoolStuff(filtPricesDf):
    # Cool things
    filtPricesDf.totAssets.min() # 82M dollars
    filtPricesDf.totAssets.max() # 2.4T dollars (JPMorgan)
