fcf = float(input("Earnings or Free Cashflow: "));

growth = float(input("Growth Rate as decimal percent: "));

rate = float(input("Discount Rate: "));

years = float(input("Years: "));

terminalPE = float(input("Terminal Multiple: "));

undiscountedPrices=[]

i = 0
thisPeriodFcf = fcf
while i < years:
    undiscountedPrices = undiscountedPrices+thisPeriodFcf
    thisPeriodFcf=thisPeriodFcf+(thisPeriodFcf*growth)


discountedPrices=[]
result=0
i = 0
while i < years:
    #discount to present
    pv = undiscountedPrices[i]/(1 + rate)**i
    discountedPrices=discountedPrices+pv
    result=result+pv
result=result+(terminalPE/(1+rate)**years)
print(result)
