import sys
fv = 0
rate = 0
period = 0
i = 0

fv = float(sys.argv[1])
#print("Future Value: ", fv)
if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) < 5:
    print("Usage:")
    print("python3 pv.py <future-value> -r <discount-rate> -p <period>")
    exit()
for arg in sys.argv:
    if i>1:
        if arg=="-p" or arg=="--period":
            period = float(sys.argv[i+1])
            #print("Period = ", period)
        if arg=="-r" or arg=="--rate":
            rate = float(sys.argv[i+1])
            #print("Rate = ", rate)
    i=i+1
pv = fv/(1 + rate)**period
print("Present Value:",pv)
