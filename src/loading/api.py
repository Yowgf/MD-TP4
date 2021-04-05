"""API for loading the dataset. The idea here is just to integrate
all of the loading procedures that the module offers into one
function.

"""

from .step1 import dfList
from .step2 import format_date, guarantee_no_nan

def allLoadPreprocess():
    for df in dfList:
        format_date(df)
        guarantee_no_nan(df)
