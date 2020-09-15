import yfinance as yf
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
#using plot3 we can plot multiple lines in a 3d space
#then using https://stackoverflow.com/questions/43217827/how-can-i-fill-an-area-below-a-3d-graph-in-matlab 
#like method we can fill in the graph

#fig = plt.figure()
def getstockmovement(ticker,intervalsel):
    #set_plot_xlimits('StockPlot',0,7)
    mystock = yf.Ticker(ticker)
    if intervalsel == '7d':
        stockmovement = mystock.history('7d',interval = '1m')
    elif intervalsel == '1mo':
        stockmovement = mystock.history('1mo','1h')
    elif intervalsel == '1y':
        stockmovement = mystock.history('1y')
    intervaldata = stockmovement['Close']
    firstprice = intervaldata[0]
    stockdata = []
    for i in range(len(intervaldata)):
        if intervalsel == '7d':
            stockdata.append([i/(len(intervaldata))*7,(intervaldata[i]-firstprice)*100/firstprice])
        else:
            stockdata.append([i,(intervaldata[i]-firstprice)*100/firstprice])
    return stockdata
def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)
def getstockslist(stocklist,intervalsel):
    masterlist = []
    for x in stocklist:
        masterlist.append(getstockmovement(x,intervalsel))
    for x in range(len(stocklist)):
        masterlist[x][-1][-1] = 0
    return masterlist
def stockplotter(tickerlist,colorlist,intervalsel):
    fig = plt.gca(projection='3d')
    numstocks = len(tickerlist) 
    maxy = 0
    miny = 0
    verts = getstockslist(tickerlist,intervalsel)
    for x in range(len(verts)):
        for y in range(len(verts[x])):
            if verts[x][y][1] > maxy:    
                maxy = verts[x][y][1]
            if verts[x][y][1] < miny:
                miny = verts[x][y][1]
    customlegend = []
    for x in range(numstocks):
        customlegend.append(mpatches.Patch(color=colorlist[x],label=tickerlist[x].upper()))
    fig.legend(handles=customlegend)
    zs = np.arange(0,numstocks,1.0)
    poly = PolyCollection(verts, facecolors=colorlist[0:numstocks],lw=0.5,edgecolor=(0,0,0,1))
    poly.set_alpha(0.5)
    poly.set_linestyle(ls='-')
    poly.set_linewidth(lw=2.0)
    fig.add_collection3d(poly,zs=zs, zdir='y')
    if intervalsel == '7d':
        fig.set_xlim3d(0,7)
        fig.set_xlabel("Time (day)")
        fig.set_zlabel("Price increase since start of week(%)")
    else:
        fig.set_xlim3d(0,len(verts[0]))
        if intervalsel == '1mo':
            fig.set_xlabel("Time (hr)")
            fig.set_zlabel("Price increase in last month(%)")
        if intervalsel == '1y':
            fig.set_xlabel("Time (day)")
            fig.set_zlabel("Price increase in last year(%)")
    #to change when understand 
    fig.set_ylabel("Stock")
    fig.set_ylim3d(0,numstocks)#set to number of stocks
    fig.set_zlim3d(miny,maxy)
    plt.show()
    plt.close('all')
def main():
    colors = [cc('r'),cc('b'),cc('c'),cc('g'),cc('m'),cc('y'),cc('k')]
    tickerlist = ['amd','msft']
    stockplotter(tickerlist,colors)
if __name__ == "__main__":
    main()
