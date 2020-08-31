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
    minutesinweek = 2709
    for i in range(len(pastweek)):
        stockdata.append([i/(minutesinweek)*7,(pastweek[i]-firstprice)*100/firstprice])
    return stockdata
def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)
def getstockslist(stocklist):
    masterlist = []
    for x in stocklist:
        masterlist.append(getstockmovement(x))
    for x in range(len(stocklist)):
        masterlist[x][-1][-1] = 0
    return masterlist
def stockplotter(tickerlist,colorlist):
    numstocks = len(tickerlist) 
    verts = getstockslist(tickerlist)
    zs = np.arange(0,numstocks,1.0)
    poly = PolyCollection(verts, facecolors=colorlist[0:numstocks])
    poly.set_alpha(0.7)
    poly.set_linestyle(ls='-')
    poly.set_linewidth(lw=2.0)
    ax.add_collection3d(poly,zs=zs, zdir='y')
    ax.set_xlabel("Time (days)")
    ax.set_xlim3d(0,7)
    ax.set_ylabel("Stock")
    ax.set_ylim3d(-1,numstocks)#set to number of stocks
    ax.set_zlabel("Price increase since start of week(%)")
    ax.set_zlim3d(0,10)
    plt.show()
    
def main():
    colors = [cc('r'),cc('b'),cc('c'),cc('g'),cc('m'),cc('y'),cc('k')]
    tickerlist = ['amd','msft']
    stockplotter(tickerlist,colors)
if __name__ == "__main__":
    main()
