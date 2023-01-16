import sys
startval = 0
endval = 0
period = 0

if len(sys.argv) < 4 or "-h" in sys.argv or "--help" in sys.argv:
    print("Calculates the CAGR given a start value, end value, and period (years).\nUsage:")
    print("python3 cagr.py <start-value> <end-value> <period>")
    exit()

startval = float(sys.argv[1])
endval = float(sys.argv[2])
period = float(sys.argv[3])
#print("Future Value: ", fv)
#for arg in sys.argv:
#    if arg=="-h" or arg=="--help":
#        print("Help")
#    if i>1:
#        if arg=="-p" or arg=="--period":
#            period = float(sys.argv[i+1])
#            #print("Period = ", period)
#        if arg=="-r" or arg=="--rate":
#            rate = float(sys.argv[i+1])
#            #print("Rate = ", rate)
#    i=i+1
#pv = fv/(1 + rate)**period

cagr = ((endval/startval)**(1/period)-1)*100
print("{:0.2f}%".format(cagr))

