fcf = float(input("Earnings or Free Cashflow: "));

growth = float(input("Growth Rate (as decimal): "));

rate = float(input("Discount Rate (as decimal): "));

years = float(input("Years: "));

terminalPE = float(input("Terminal Multiple: "));

undiscountedPrices=[]

i = 0
thisPeriodFcf = fcf
lastFcf=0
while i < years:
    if(i==years-1):
        thisPeriodFcf=thisPeriodFcf*terminalPE
    undiscountedPrices.append(thisPeriodFcf)
    print(thisPeriodFcf)
    lastFcf=thisPeriodFcf
    thisPeriodFcf=thisPeriodFcf+(thisPeriodFcf*growth)
    i=i+1

discountedPrices=[]
result=0
i = 1 #skip first year (which was last year)
while i < years:
    #discount to present
    pv = undiscountedPrices[i]/(1 + rate)**i
    discountedPrices.append(pv)
    print(pv)
    result=result+pv
    i=i+1
#result=result+(terminalPE/(1+rate)**years)
print('Intrinsic Value:',result)
