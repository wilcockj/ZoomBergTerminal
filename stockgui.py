from dearpygui.dearpygui import *
from math import cos, sin
import yfinance as yf
#idea same process but matlab 3d graph to compare stocks would look really cool
#x is time
#z is price/percent change
#y is which number of stock
#add a textbox to search a stock ticker and generate a graph of price
#add functionality to keep adding more stocks
#scale graph by percent differnce from the start of the time period
add_input_text("Stock Ticker", default_value="msft")
add_color_picker3("colorpicker3",width=100)
add_button("Plot data", callback="plot_callback")
add_plot("StockPlot", "Time (day)", "Increase from Start of Week (%)", height=-1)
add_data("maxy", 0)
add_data("miny", 0)
#use these variables to keep track of limits
#make sure ot keep each stock in range
show_documentation()
show_logger()
#set x limit 0-7
#set y limit -10% over 10% over high and low
#set_plot_x,ylimits()
#need to look for max of whole plot 
def color_generator():
    colors =[(102,153,255),(204, 0, 0),(204, 102, 255),(51, 204, 51),(255, 204, 153)]
    num = 0
    while True:
        yield colors[num]
        num += 1
        log_debug(num)
        if(num > len(colors)-1):
            log_debug("relooping")
            num = 0
gen = color_generator()

def plot_callback(sender, data):
    #try except for if the ticker is correct
    #clear_plot("StockPlot")
    set_plot_xlimits('StockPlot',0,7)
    mystock = yf.Ticker(get_value('Stock Ticker'))
    stockmovement = mystock.history('7d',interval = '1m')
    print(get_value("colorpicker3"))
    if stockmovement.empty:
        print("bad ticker")
    else:
        print(stockmovement)
        pastweek = stockmovement['Close']
        firstprice = pastweek[0]
        set_plot_ylimits('StockPlot',(pastweek.min()-firstprice)*100/firstprice,(pastweek.max()-firstprice)*100/firstprice)
        if maxy[0] < (pastweek.max()-firstprice)*100/firstprice:
            maxy[0] = (pastweek.max()-firstprice)*100/firstprice
        if miny[0] > (pastweek.min()-firstprice)*100/firstprice:
            miny[0] = (pastweek.min()-firstprice)*100/firstprice
        #set_plot_ylimits('StockPlot',(pastweek.min()-firstprice)*100/firstprice,(pastweek.max()-firstprice)*100/firstprice)
        set_plot_ylimits('StockPlot',miny[0],maxy[0])   
        print((pastweek.min()-firstprice)*100/firstprice,(pastweek.max()-firstprice)*100/firstprice)
        weeklist = []
        #make the price percent change from start
        for i in range(len(pastweek)):
            weeklist.append((i/(2709)*7,(pastweek[i]-firstprice)*100/firstprice))
        newcolor = next(gen)
        print(newcolor)
        add_line_series("StockPlot", get_value('Stock Ticker'), weeklist, weight=2, fill=[get_value("colorpicker3"), 100])
    #add_scatter_series("Plot", "test", weeklist)



maxy = [0]
miny = [0]
start_dearpygui()
