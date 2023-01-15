import sys

capital = 0
addition = 0
rate = 0
years = 0

if len(sys.argv) <= 1:
    capital = float(input("Enter starting capital: "));
    addition = float(input("Enter annual contribution: "));
    rate = float(input("Enter rate of return: "));
    years = float(input("Enter years to grow: "));
else:
    i=0
    if(sys.argv[1]!="-h"):
            capital = float(sys.argv[1])
    for arg in sys.argv:
        if arg=="-h":
            print("-r\tsets rate as decimal.")
            print("-y\thow many years to compound. -p for periods is also valid.")
            print("-c\tamount to contribute each period (optional)")
            print("Usage:")
            print("[python3] compound[.py] 10000 -r 0.1 -y 10 -c 10000 ")
            print("Compound $10,000 at 10% for 10 years, contributing an additional $10,000 each year.")
            exit()
        if arg=="-r":
            rate = float(sys.argv[i+1])
        if arg=="-y" or arg=="-p":
            years = int(sys.argv[i+1])
            print("Setting years to:",sys.argv[i+1])
        if arg=="-c" or arg=="-a" or arg=="--contribution":
            addition = float(sys.argv[i+1])
        i=i+1
print("Rate:",rate)
print("Years:",years)
costbasis = capital;

i = 0;
while i < years:
    capital = capital + (capital*(rate))
    capital = capital + addition
    costbasis = costbasis + addition
    print("End of year ",i+1,": ",int(capital))
    print("Cost basis",int(costbasis))
    i=i+1
