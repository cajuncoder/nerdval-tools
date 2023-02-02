import sys
import yfinance as yf
import pandas as pd
import os
pd.options.display.float_format = '{:.2f}'.format #Suppress scientific notation of numbers

ticker = sys.argv[1]

SHOW_NAME = False
SHOW_CURRENCY = False
if('-h' in sys.argv):
    print('-n\tshow security name')
    print('-c\tshow currency')
    exit()
if('-n' in sys.argv):
    SHOW_NAME = True
if('-c' in sys.argv):
    SHOW_CURRENCY = True
tickerDataFetcher = yf.Ticker(ticker)

company=tickerDataFetcher
print(company.balance_sheet)

#use "fast_info" instead of "info" now.
company=tickerDataFetcher.fast_info
#print(company) #<---debugging when API breaks
name=ticker#company['shortName']
currency=company['currency']
price=round(float(company['last_price']),2)
if SHOW_NAME:
    print(name)
if not SHOW_CURRENCY:
    print(price)
else:
    print(price, currency)
