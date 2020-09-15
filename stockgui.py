from dearpygui.dearpygui import *
from math import cos, sin
import yfinance as yf
import stockgraph3d as sg
#TODO
#add detector for changing of the interval option that regraphs the stocks
#idea same process but matlab 3d graph to compare stocks would look really cool
#x is time
#z is price/percent change
#y is which number of stock
#add a textbox to search a stock ticker and generate a graph of price
#add functionality to keep adding more stocks
#scale graph by percent differnce from the start of the time period
set_theme("Dark Grey")
set_main_window_title("ZoomBerg Terminal")
add_input_text("Stock Ticker", default_value="msft",width = 100)
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
#use these variables to keep track of limits
#make sure ot keep each stock in range
#set x limit 0-7
#set y limit -10% over 10% over high and low
#set_plot_x,ylimits()
#need to look for max of whole plot 
#possibly change to regraph all current tickers for the new interval
def changedinterval(sender,data):
    tickerlist.clear()
    clear_plot("StockPlot")
    maxy[0] = 0
    miny[0] = 0
def opendocs(sender,data):
    show_documentation()
def openlogger(sender,data):
    show_logger()
def plotter3d(sender, data):
    #here call something to use the 3d plotter
    log_debug("Inside 3d plotting function")
    colorlist = []
    tickers = []
    log_debug(tickerlist)
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
    close_popup()
def plot_callback(sender, data):
    #print(tickerlist)
    #try except for if the ticker is correct
    #clear_plot("StockPlot")
    ticker = get_value('Stock Ticker')
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
            show_item("Ticker Error")
        else:    
            add_popup("Plot stock history","Ticker Error", modal=True)
            add_text("Invalid Ticker")
            add_button("Ok", callback="close_window")
            end_popup()
    else:
        newcolor = get_value("Choose Color Of Stock")
        fixedcolor = []
        for y in range(4):
            fixedcolor.append(float(int(newcolor[y])/255))
        tickerlist[ticker] = fixedcolor
        pastweek = stockmovement['Close']
        firstprice = pastweek[0]
        log_debug(f"the length of the plotting is {len(pastweek)}")
        if intervalsel == '7d':
            set_plot_xlimits('StockPlot',0,7)
        else:
            set_plot_xlimits('StockPlot',0,len(pastweek)-1)
        set_plot_ylimits('StockPlot',(pastweek.min()-firstprice)*100/firstprice,(pastweek.max()-firstprice)*100/firstprice)
        if maxy[0] < (pastweek.max()-firstprice)*100/firstprice:
            maxy[0] = (pastweek.max()-firstprice)*100/firstprice
        if miny[0] > (pastweek.min()-firstprice)*100/firstprice:
            miny[0] = (pastweek.min()-firstprice)*100/firstprice
        log_debug(f"{miny[0],maxy[0]}")
        set_plot_ylimits('StockPlot',miny[0],maxy[0])   
        weeklist = []
        #make the price percent change from start
        if intervalsel == '7d':
            for i in range(len(pastweek)):
                weeklist.append((i/(2709)*7,(pastweek[i]-firstprice)*100/firstprice))
        else:
            for i in range(len(pastweek)):
                weeklist.append((i,(pastweek[i]-firstprice)*100/firstprice))
        add_line_series("StockPlot", ticker.upper(), weeklist, weight=2, fill=[newcolor[0],newcolor[1],newcolor[2], 100])
    #add_scatter_series("Plot", "test", weeklist)


tickerlist = {}
maxy = [0]
miny = [0]
start_dearpygui()
