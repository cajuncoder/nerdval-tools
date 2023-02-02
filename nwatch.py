#TODO: Add --vertical option implementation
#TODO: Allow configuration of default watchlist in ~/.watchlist file? 
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
WHITE = '\033[37m'
RESET = '\033[39m'


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
		leftover=int(spacing-len(strings[i]))
		line=line+strings[i]+' '*leftover	
	print(color+line+ENDC)

def printSpacedRightAligned(strings, spacing):
	line=""
	leftover=0
	for i in range(0,len(strings)):
		strings[i]=str(strings[i])
		strings[i] = (strings[i][:spacing-3] + '..') if len(strings[i]) > spacing-1 else strings[i]
		leftover=int(spacing-len(strings[i]))
		line=line+' '*leftover+strings[i]	
	print(line)

# #ticker = sys.argv[1]
# tickers = ['AAPL', 'GOOGL', 'INTC']
# tickerDataFetcher = yf.Ticker(tickers)
# company=tickerDataFetcher.info
terminalWidth = 80
nOfDisplayCols = 4
SHOW_PE = False
SHOW_DIV = False
VERTICAL = False
GET_INFO = False
CHEAP_ONLY = False
csvFile = ''

USAGE = 'Usage: "python3 watchlist.py <tsv or csv file>"'
if len(sys.argv) < 2 or sys.argv[1].startswith('--'):
    if os.path.isfile(os.path.expanduser('~/.nwatch')):
        f = open(os.path.expanduser('~/.nwatch'),'r')
        csvFile=f.readline().strip()
        f.close()
    else:
	    print('--pe\tshow pe ratio [broken]')
	    print('--div\tshow dividend info [broken]')
	    print('--all\tshow all info [broken]')
	    print('--cheap-only\tshow only stocks near or below intrinsic value')
	    print('--get-info\tshow company info [requires "ninfo.py" to be in path]')
	    print('--width\tset terminal width')
	    print('--vertical\tlist info for each stock vertical instead of horizontal')
	    print('--help\tprint this message')

	    print(USAGE)
	    exit()
if '-h' in sys.argv or '--help' in sys.argv:
	print('-width\tset terminal width')
	print('-v\tlist info for each stock vertical instead of horizontal')
	print('-h\tprint this message')
	print(USAGE)
	exit()
if '--cheap-only' in sys.argv:
    CHEAP_ONLY = True
if '--get-info' in sys.argv:
    GET_INFO = True
if '--vertical' in sys.argv:
	VERTICAL = True
if '--width' in sys.argv:
	terminalWidth = int(sys.argv[sys.argv.index('-width')+1])
spacing = int(terminalWidth/nOfDisplayCols)
if not csvFile:
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
#spacing=24
i = 0

displayCols = ['Ticker','Price','IntrVal', 'MOS']
printSpaced(displayCols, spacing)

for symbol in watchlist_symbols:
    info=tickers.tickers[symbol].fast_info
    price=round(info['last_price'],2)
    intrinsic=watchlist_intrinsic_vals[i]
    MOSamt=round(float(intrinsic)-float(price),2)
    MOS=round(MOSamt/price*100,0)
    IS_CHEAP = False

    #get color
    color = RESET
    if MOS >= -5 and MOS < 0:
        color = RESET
    elif MOS >= 0:
        color = CGREEN
        IS_CHEAP = True
    else:
        color = CRED
    if IS_CHEAP and CHEAP_ONLY:
        displayFields = [symbol,price,intrinsic,MOS]
        printSpacedColored(displayFields, spacing,color)
        if GET_INFO:
            os.system('python3 '+os.path.dirname(__file__)+'/ninfo.py '+symbol)
    elif not CHEAP_ONLY:
        displayFields = [symbol,price,intrinsic,MOS]
        printSpacedColored(displayFields, spacing,color)
        if GET_INFO:
            os.system('python3 '+os.path.dirname(__file__)+'/ninfo.py '+symbol)

    i=i+1
