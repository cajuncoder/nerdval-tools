#watchlist2.py

import sys
import yfinance as yf
import pandas as pd
import os
import csv
pd.options.display.float_format = '{:.2f}'.format #Suppress scientific notation of numbers

CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
ENDC = '\033[0m'


def printSpaced(strings, spacing):
	line=""
	leftover=0
	for i in range(0,len(strings)):
		strings[i]=str(strings[i])
		strings[i] = (strings[i][:spacing-3] + '..') if len(strings[i]) > spacing-1 else strings[i]
		leftover=spacing-len(strings[i])
		line=line+strings[i]+' '*leftover	
	print(line)

def printSpacedColored(strings, spacing, color):
	line=""
	leftover=0
	for i in range(0,len(strings)):
		strings[i]=str(strings[i])
		strings[i] = (strings[i][:spacing-3] + '..') if len(strings[i]) > spacing-1 else strings[i]
		leftover=spacing-len(strings[i])
		line=line+strings[i]+' '*leftover	
	print(color+line+ENDC)

def printSpacedRightAligned(strings, spacing):
	line=""
	leftover=0
	for i in range(0,len(strings)):
		strings[i]=str(strings[i])
		strings[i] = (strings[i][:spacing-3] + '..') if len(strings[i]) > spacing-1 else strings[i]
		leftover=spacing-len(strings[i])
		line=line+' '*leftover+strings[i]	
	print(line)

# #ticker = sys.argv[1]
# tickers = ['AAPL', 'GOOGL', 'INTC']
# tickerDataFetcher = yf.Ticker(tickers)
# company=tickerDataFetcher.info

csvFile = sys.argv[1]
csvTickerCol = 0
csvIntrinsicCol = 1
csvCurrencyCol = 2
csvStartLine = 1

watchlist_symbols = []
watchlist_intrinsic_vals = []
watchlist_currency = []

with open(csvFile, 'r') as file:
  csvreader = csv.reader(file, delimiter='\t')
  line=0
  for row in csvreader:
    if line >= csvStartLine:
      watchlist_symbols.append(row[csvTickerCol])
      watchlist_intrinsic_vals.append(row[csvIntrinsicCol])
      watchlist_currency.append(row[csvCurrencyCol])
    line+=1



tickers = yf.Tickers(watchlist_symbols)
# ^ returns a named tuple of Ticker objects

# access each ticker using (example)
# tickers.tickers.MSFT.info
# tickers.tickers.AAPL.history(period="1mo")
# tickers.tickers.GOOG.actions
# name=company['shortName']
# currency=company['currency']
# shares=company['sharesOutstanding']
# price=company['regularMarketPrice']
# for tkr in tickers.tickers:
# 	print(tkr.info['shortName'])
# 	print(tkr.info['regularMarketPrice'])
spacing=24
i = 0
printSpaced(['Company','Ticker','Price','Intrinsic Value', 'Margin of Safety','Forward PE', 'Dividend Yield', 'Payout Ratio'], spacing)
for symbol in watchlist_symbols:
    info=tickers.tickers[symbol].info
    price=info['regularMarketPrice']  #round(prices[i]['Close'][day],2)
    intrinsic=watchlist_intrinsic_vals[i]   #round(float(watchlist_intrinsic_vals[i]),2)
    MOSamt=round(float(intrinsic)-float(price),2)
    MOS=round(MOSamt/price*100,0)
    fwPe=info['forwardPE']
    div=info['dividendYield']
    payout=info['payoutRatio']
    #current=info['currentRatio']
    if MOS >= -5 and MOS < 10:
        printSpaced([info['shortName'],symbol,info['regularMarketPrice'],intrinsic,MOS,fwPe, div, payout], spacing)
    elif MOS >= 10:
        printSpacedColored([info['shortName'],symbol,info['regularMarketPrice'],intrinsic,MOS,fwPe, div, payout], spacing,CGREEN)
    else:
        printSpacedColored([info['shortName'],symbol,info['regularMarketPrice'],intrinsic,MOS,fwPe, div, payout], spacing,CRED)
    # print(info['shortName'])
    # print(info['regularMarketPrice'])
    # print(info['currency'])
    i=i+1
