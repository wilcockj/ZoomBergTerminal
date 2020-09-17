from dearpygui.dearpygui import *
from math import cos, sin
import yfinance as yf
import stockgraph3d as sg
#TODO
#stop ability to replot a stock, looks confusing
#figure out how the plotting is being done and if ticker in tickerlist dont plot
#easy to stop replotting but removes ability to change color of stock which is a nice feature,
#if that is removed should make a new dialouge where user can change color of a certain stock
#improve gui look make some things on the same line to not leave as much blank space on the right
#x is time
#z is price/percent change
#y is which number of stock
#add a textbox to search a stock ticker and generate a graph of price
set_theme("Dark Grey")
set_main_window_title("ZoomBerg Terminal")
add_input_text("Input Stock Ticker", default_value="msft",width = 100)
add_spacing(count=4)
add_color_picker3("Choose Color Of Stock",width=100)
add_button("Plot stock history", callback="plot_callback")
add_button("Clear plot", callback="plot_clearer")
add_button("Plot in 3d", callback="plotter3d")
add_combo("Select Plotting Interval",['7d','1mo','1y'],width = 100, default_value = '7d', callback = "changedinterval")
add_button("Open logger", callback="openlogger")
add_same_line()
add_button("Open dearpygui documentation", callback="opendocs")
add_plot("StockPlot", "Time Interval", f"Increase from Start of Time Interval (%)", height=-1)
add_data("maxy", 0)
add_data("miny", 0)

#possibly change to regraph all current tickers for the new interval
def changedinterval(sender,data):
    clear_plot("StockPlot")
    maxy[0] = 0
    miny[0] = 0
    for item in tickerlist.items():
        plotfunc(item[0],item[1])

def opendocs(sender,data):
    show_documentation()

def openlogger(sender,data):
    show_logger()

def plotter3d(sender, data):
    log_debug("Inside 3d plotting function")
    colorlist = []
    tickers = []
    intervalsel = get_value("Select Plotting Interval")
    for x,y in tickerlist.items():
        tickers.append(str(x))
        colorlist.append(y)
    log_debug(tickers)
    if tickers:
        sg.stockplotter(tickers,colorlist,intervalsel)

def plot_clearer(sender, data):
    tickerlist.clear()
    clear_plot("StockPlot")
    maxy[0] = 0
    miny[0] = 0

def close_window(sender,data):
    hide_item("Ticker Error")
    set_theme("Dark Grey")

def plot_callback(sender, data):
    ticker = get_value('Input Stock Ticker')
    plotfunc(ticker,0)

def plotfunc(ticker,color):
    mystock = yf.Ticker(ticker)
    intervalsel = get_value("Select Plotting Interval")
    log_debug(f"{intervalsel}")
    if intervalsel == '7d':
        stockmovement = mystock.history('7d',interval = '1m')
    elif intervalsel == '1mo':
        stockmovement = mystock.history('1mo',interval = '1h')
    elif intervalsel == '1y':
        stockmovement = mystock.history('1y')
    if stockmovement.empty:
        if does_item_exist("Ticker Error"):
            set_theme("Red")
            show_item("Ticker Error")
        else:    
            #add_popup("Plot stock history","Ticker Error", modal=True)
            add_window("Ticker Error",width = 200, height = 90)
            set_theme("Red")
            add_text("Invalid Ticker")
            add_button("Ok", callback="close_window")
            end_window()
    else:
        if color == 0:
            newcolor = get_value("Choose Color Of Stock")
            log_debug(f"chosen color {newcolor}")
            fixedcolor = []
            for y in range(4):
                fixedcolor.append(float(int(newcolor[y])/255))
            tickerlist[ticker] = fixedcolor
        else:
            fixedcolor = color
            newcolor = (color[0]*255,color[1]*255,color[2]*255,color[3]*255)
            log_debug(f"before: {color}")
            log_debug(f"after: {newcolor}")
        intervaldata = stockmovement['Close']
        firstprice = intervaldata[0]
        log_debug(f"the length of the plotting is {len(intervaldata)}")
        if intervalsel == '7d':
            set_plot_xlimits('StockPlot',0,7)
        else:
            set_plot_xlimits('StockPlot',0,len(intervaldata)-1)
        set_plot_ylimits('StockPlot',(intervaldata.min()-firstprice)*100/firstprice,(intervaldata.max()-firstprice)*100/firstprice)
        if maxy[0] < (intervaldata.max()-firstprice)*100/firstprice:
            maxy[0] = (intervaldata.max()-firstprice)*100/firstprice
        if miny[0] > (intervaldata.min()-firstprice)*100/firstprice:
            miny[0] = (intervaldata.min()-firstprice)*100/firstprice
        log_debug(f"{miny[0],maxy[0]}")
        set_plot_ylimits('StockPlot',miny[0],maxy[0])   
        datalist = []
        #graph percent change from start
        if intervalsel == '7d':
            for i in range(len(intervaldata)):
                datalist.append((i/(2709)*7,(intervaldata[i]-firstprice)*100/firstprice))
        else:
            for i in range(len(intervaldata)):
                datalist.append((i,(intervaldata[i]-firstprice)*100/firstprice))
        add_line_series("StockPlot", ticker.upper(), datalist, weight=2, fill=[newcolor[0],newcolor[1],newcolor[2], 100])

tickerlist = {}
maxy = [0]
miny = [0]
start_dearpygui()
