"""Basic graphical visualizations are implemented here.

"""

from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = (8, 6)
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.labelsize"] = "large"

ibmData = None
foxData = None

def plotOpenPriceSeries(pricesDf):
    global ibmData, foxData
    
    plt.figure(1)
    plt.xlabel("day")
    plt.ylabel("US$")

    # Plot first data for IBM company
    ibmData = pricesDf[pricesDf["symbol"] == "IBM"]
    plt.plot(ibmData.date, ibmData.open, label="IBM")

    # Plot the mean of the NYSE overall opening prices
    stockPricesSeries = pricesDf.groupby(["date"]).mean()["open"]
    plt.plot(stockPricesSeries.index, stockPricesSeries.values, label="NYSE (mean)")

    # Plot data for FOX company
    foxData = pricesDf[pricesDf["symbol"] == "FOX"]
    plt.plot(foxData.date, foxData.open, label="FOX")

    plt.legend()
    plt.savefig("doc/data-frames/open-price-series.png")
    plt.show()

def plotIbmFoxVolumes(pricesDf):
    global ibmData, foxData

    # Plot volume of trades for the FOX company
    plt.figure(1)
    plt.xlabel("day")
    plt.ylabel("traded stock volume")
    plt.plot(ibmData.date, ibmData.volume)
    plt.savefig("doc/data-frames/ibm-volume.png")

    # Same for the IBM company
    plt.figure(2)
    plt.xlabel("day")
    plt.ylabel("traded stock volume")
    plt.plot(foxData.date, foxData.volume)
    plt.savefig("doc/data-frames/fox-volume.png")

    plt.show()
