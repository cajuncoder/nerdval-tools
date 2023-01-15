import sys
import yfinance as yf
import pandas as pd
import os
pd.options.display.float_format = '{:.2f}'.format #Suppress scientific notation of numbers

# make tools calculate:
# ROCE (Operating Income / Capital Employed)
# Cap. Employed = total assets - excess cash - non interest bearing current liabilities
# non interest bearing current liabilities = accounts payable, deferred income, accrued expenses
# keep financial debt IN the calculation
# is all cash unnecessary? how much to subtract

# Calculate the following:
# 1. ROCE
# 2. FCFROCE
# 3. Growth of Operating Income per Fully Diluted Share (DELTA OI/FDS)
# 4. Growth in Free Cashflow per Fully Diluted Share (DELTA FCF/FDS)
# 5. DELTA BV/FDS (or BV+Dividends/FDS)
# 6. DELTA TBV/FDS
# 7. Liabilities to Equity Ratio ***Preference, Total Liabilities / BV
# 8. Interest Coverage Ratio 
# 9. Debt to Equity Ratio
# 10. Current Ratio
# 11. Normalized 4 year earnings?

# Financial Figures needed:
# (Income Statement)
# Operating Income
# Interest Expense? *Not a must
# (Cashflow Statement)
# Cashflow From Operations
# Capital Expenditures
# (Balance Sheet)
# Cash
# Goodwill
# Intangible Assets
# Total Assets
# Accounts Payable
# Deferred Income
# Accrued Expenses
# Total Liabilities
# Shareholders Equity
# Fully Diluted Shares
# Effective Tax Rate? *Not a must

COMPACT = False
ticker = sys.argv[1]

tickerDataFetcher = yf.Ticker(ticker)
print(tickerDataFetcher.info)
company=tickerDataFetcher.info
#print(company.info)
#print(company.calendar)
#print(company.earnings)
#print(company.cashflow)
#print(company.financials)
#print(company.balance_sheet)
#print(company.financials) #cashflow statement
#print(company.financials)
name=company['shortName']
currency=company['currency']
shares=company['sharesOutstanding']
price=company['regularMarketPrice']
current_ratio=company['currentRatio']
dividend_rate=company['dividendRate']
dividend_yield=company['dividendYield']
payout_ratio=company['payoutRatio']
book_val=company['bookValue']
forward_eps=company['forwardEps']
trailing_eps=company['trailingEps']
long_business_summary=company['longBusinessSummary']
if COMPACT: long_business_summary=(long_business_summary[:360] + '..') if len(long_business_summary) > 360 else long_business_summary
debt_to_equity=company['debtToEquity']
return_on_equity=company['returnOnEquity']
earnings_growth=company['earningsGrowth']

def printSpaced(strings, spacing):
	line=""
	leftover=0
	for i in range(0,len(strings)):
		strings[i]=str(strings[i])
		strings[i] = (strings[i][:spacing-3] + '..') if len(strings[i]) > spacing-1 else strings[i]
		leftover=spacing-len(strings[i])
		line=line+strings[i]+' '*leftover	
	print(line)

def printSpacedRightAligned(strings, spacing):
	line=""
	leftover=0
	for i in range(0,len(strings)):
		strings[i]=str(strings[i])
		strings[i] = (strings[i][:spacing-3] + '..') if len(strings[i]) > spacing-1 else strings[i]
		leftover=spacing-len(strings[i])
		line=line+' '*leftover+strings[i]	
	print(line)





# COMPANY NAME, CHART
col_spacing=20
printSpaced([name, company['industry']],32)
#priceData=tickerDataFetcher.history(period="max",frequency="monthly")
priceData=tickerDataFetcher.history(period="max")
maxPrice=0
minPrice=999999999999999999999999999

width=int(os.get_terminal_size().columns-9)#120
#if COMPACT: width=80-7
height=int(os.get_terminal_size().lines/2)
#if COMPACT: height=12

#print(priceData)
priceArray=[]
datesArray=[]
for val in priceData['Close']:
	priceArray.append(val)

for date, row in priceData.iterrows():
	datesArray.append(date)

tradingDays=252
numOfYearsToChart=5
if COMPACT: numOfYearsToChart=5
yearLen=(tradingDays/width)
skipDays=int(yearLen*numOfYearsToChart) #120*15/365 = 5y
counter=0
width_scaled=int((width*(skipDays)))

print(round(width_scaled/tradingDays,1),' Year Chart:')

for y in range(height,-1, -1):
	priceRange=0
	scaleMulti=0
	starti = (len(priceArray))-width_scaled
	for g in range(starti,starti+width_scaled):
		#print(len(priceArray))
		#print(g)
		if priceArray[g] > maxPrice:
			maxPrice=priceArray[g]
		if priceArray[g] < minPrice:
			minPrice=priceArray[g]
		#print('Min price',minPrice)
		#print('Max price',maxPrice)
		priceRange=maxPrice-minPrice
	for x in range(0,width_scaled):
		counter=counter+1
		if counter >= skipDays:
			c = ' '
			scaleMulti=height/priceRange
			pp = float(priceArray[starti+x]-minPrice)*scaleMulti
			if y < pp:
				c = '#'
			counter=0
			print(c,end='')
	print(' ',round((y*(priceRange/height)+minPrice),2))



#'2022-10'
skip_chars=7
skip_step=7
spacing=7
space_counter=0
counter=0
starti = (len(priceArray))-width_scaled

#print dates
for x in range(0,width_scaled):
	counter=counter+1
	if counter >= skipDays:
		# print('X',end='')
		string = ' '
		skip_step = skip_step+1
		if space_counter >= spacing and skip_step >= skip_chars:
			string=str(datesArray[starti+x])
			print(string[0:7],end='')
			skip_step = 0
			space_counter = 0
		elif skip_step >= skip_chars:
			space_counter=space_counter+1
			print(' ',end='')
		# if space_counter >= spacing:
		# 	print('-',end='')
		# 	#space_counter=0
		counter=0

print()
if not COMPACT: print()
print(long_business_summary)
if not COMPACT: print()
printSpaced(['Current Price',price,currency],col_spacing)
printSpaced(['Forward EPS', forward_eps,'Forward PE',price/forward_eps],col_spacing)
printSpaced(['Trailing EPS', trailing_eps, 'Trailing PE',price/trailing_eps],col_spacing)
printSpaced(['Dividend Yield', str(dividend_yield), 'Dividend Payout Ratio', str(payout_ratio)],col_spacing)
#printSpaced(['Dividend Payout Ratio', str(payout_ratio)],col_spacing)
if not COMPACT: print()
printSpaced(['Revenue Growth', company['revenueGrowth'],'Earnings Growth', earnings_growth],col_spacing)
#printSpaced(['Earnings Growth', earnings_growth], col_spacing)
if not COMPACT: printSpaced(['Earnings Q. Growth', company['earningsQuarterlyGrowth'],'Return on Equity',str(return_on_equity)], col_spacing)
if not COMPACT: print()
#printSpaced(['Return on Equity',str(return_on_equity)],col_spacing)
printSpaced(['Current Ratio',current_ratio,'Debt to Equity Ratio', str(debt_to_equity)+'%'],col_spacing)
#printSpaced(['Debt to Equity Ratio', str(debt_to_equity)+'%'],col_spacing)
if not COMPACT: printSpaced(['Shares Outstanding', shares],col_spacing)
print()
if not COMPACT:
	printSpacedRightAligned(['Total Revenue',company['totalRevenue']],col_spacing)
	printSpacedRightAligned(['Free Cashflow',company['freeCashflow']],col_spacing)
	printSpacedRightAligned(['Total Cash',company['totalCash']],col_spacing)
	printSpacedRightAligned(['Total Debt',company['totalDebt']],col_spacing)



#print(tickerDataFetcher.history(period="max",frequency="monthly"))

# print(name)
# print(long_business_summary)
# print(shares)
# print(currency)
# print(price)
# print(dividend_yield)
# print(forward_eps)


# for key in company.financials:
# 	print(company.financials[key]['Net Income']," ",key)
# 	print((float(company.financials[key]['Net Income'])/shares)," ",key)

# aapl = yf.Ticker("INTC")

# # get stock info
# aapl.info
 
# # get historical market data
# hist = aapl.history(period="max")
 
# # show actions (dividends, splits)
# aapl.actions
 
# # show dividends
# aapl.dividends
 
# # show splits
# aapl.splits
 
# # show financials
# aapl.financials
# aapl.quarterly_financials
 
# # show major holders
# aapl.major_holders
 
# # show institutional holders
# aapl.institutional_holders
 
# # show balance sheet
# print(aapl.balance_sheet)
# print(company.quarterly_balance_sheet)
 
# # show cashflow
# aapl.cashflow
# aapl.quarterly_cashflow
 
# # show earnings
# aapl.earnings
# aapl.quarterly_earnings
 
# # show sustainability
# aapl.sustainability
 
# # show analysts recommendations
# aapl.recommendations
 
# # show next event (earnings, etc)
#aapl.calendar
 
# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# aapl.isin
 
# # show options expirations
# aapl.options
 
# # get option chain for specific expiration
# #opt = aapl.option_chain('YYYY-MM-DD')
