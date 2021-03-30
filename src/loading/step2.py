"""Implements basic formatting procedures, necessary even to
visualize the data.

At first, only the "date" column needed to be changed.

"""

# Realizar formatacao basica dos dados
# colunas a serem formatadas = ["date"]
from pandas import to_datetime
from numpy import int64

# Defined in format_date
minDate = None
maxDate = None

def date_to_day(dtObj):
    nanosToS = lambda nano: nano / 1e9
    sToHours = lambda s: s / 3600
    hoursToDays = lambda h: h / 24

    # Composition
    nanosToDays = lambda nanos: hoursToDays(sToHours(nanosToS(nanos)))
    
    return nanosToDays(dtObj.value)

# Convert every date in the given series to have base on the minumum date
# That is to say that the minimum date will be day 0, for example
def normalize_date(dateSeries, minDate):
    return dateSeries - minDate

def format_date(df, dateCol="date"):
    df[dateCol] = to_datetime(df[dateCol])

    # Guardar estes valores, caso seja necessario depois
    global minDate, maxDate
    minDate = df[dateCol].min()
    maxDate = df[dateCol].max()
    
    # Convert every date to a day by day format
    df[dateCol] = normalize_date(df[dateCol], minDate)
    
    df[dateCol] = df[dateCol].apply(date_to_day).astype(int64)

# Checks for Nan, None, np.NaN
def guarantee_no_nan(df):
    assert(df.isna().values.sum() == 0)

def check_all_dfs_no_nan(dfsList):
    for df in dfsList:
        guarantee_no_nan(df)
