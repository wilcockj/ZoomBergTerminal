import yfinance as yf
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
#using plot3 we can plot multiple lines in a 3d space
#then using https://stackoverflow.com/questions/43217827/how-can-i-fill-an-area-below-a-3d-graph-in-matlab 
#like method we can fill in the graph

fig = plt.figure()
ax = fig.gca(projection='3d')

def getstockmovement(ticker):
    #set_plot_xlimits('StockPlot',0,7)
    mystock = yf.Ticker(ticker)
    stockmovement = mystock.history('7d',interval = '1m')
    pastweek = stockmovement['Close']
    firstprice = pastweek[0]
    stockdata = []
    for i in range(len(pastweek)):
        stockdata.append([i/(2709)*7,(pastweek[i]-firstprice)*100/firstprice])
    return stockdata
def cc(arg):
    print(f"cc called {arg}")
    return mcolors.to_rgba(arg, alpha=0.6)
def main():
    numstocks = 2
    zs = np.arange(0,numstocks,1.0)
    #print(zs)
    msftdata = getstockmovement('msft')
    amddata = getstockmovement('amd')
    masterlist = [] 
    #amddata[-1][-1] = 0
    #msftdata[-1][-1] = 0
    #print(amddata)
    verts = []
    #print(msftdata[0])
    verts.append(msftdata)
    verts.append(amddata)
    #print(verts)   
    poly = PolyCollection(verts, facecolors=[cc('r'), cc('g')])
    #poly.set_color
    poly.set_alpha(0.7)
    ax.add_collection3d(poly,zs=zs, zdir='y')
    ax.set_xlabel("Time (days)")
    ax.set_xlim3d(0,7)
    ax.set_ylabel("Stock")
    ax.set_ylim3d(-1,numstocks)#set to number of stocks
    ax.set_zlabel("Price increase since start of week(%)")
    ax.set_zlim3d(0,10)
    plt.show()
if __name__ == "__main__":
    main()
