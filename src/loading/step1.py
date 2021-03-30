"""MD-TP4 project. Loading procedures.

This file implements procedures to load any of the files in the nyse
dataset, that comprises of a total of 4 different csv files. In this
project, we will probably only use the file 'prices.csv', but the
implementation is done such as to allow very easy extension in later
phases of the project.

Note that some global variables are defined here.

"""

from pandas import read_csv

data_dir = None
dataset_names = None
    
def load_csv(file, data_dir="data"):
    return read_csv(data_dir + "/" + file)

def load_all(dfNamesList):
    global data_dir, dataset_names
    data_dir = "data"
    
    fundamentals = load_csv("fundamentals.csv")
    prices = load_csv("prices.csv")
    prices_split_adjusted = load_csv("prices-split-adjusted.csv")
    securities = load_csv("securities.csv")

    nameToDf = {"fundamentals": fundamentals,
               "prices": prices,
               "prices_split_adjusted": prices_split_adjusted,
               "securities": securities}
    
    if dfNamesList == []:
        raise AttributeError("Empty names list.")
    
    dataset_names = dfNamesList
    if len(dfNamesList) == 1:
        return nameToDf[dfNamesList[0]]
    else:
        return [nameToDf[name] for name in dfNamesList]

# Global
pricesDf = load_all(["prices"]) # Only deal with prices for now
# Define this list so to be used later if needed
dfList = [pricesDf]
