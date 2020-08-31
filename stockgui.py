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
    print(get_plot_query_area('StockPlot'))
    set_plot_xlimits('StockPlot',0,7)
    mystock = yf.Ticker(get_value('Stock Ticker'))
    stockmovement = mystock.history('7d',interval = '1m')
    print(stockmovement)
    pastweek = stockmovement['Close']
    firstprice = pastweek[0]
    set_plot_ylimits('StockPlot',(pastweek.min()-firstprice)*100/firstprice,(pastweek.max()-firstprice)*100/firstprice)
    if get_value("maxy") < (pastweek.max()-firstprice)*100/firstprice:
        set_value("maxy",(pastweek.max()-firstprice)*100/firstprice)
    if get_value("miny") > (pastweek.min()-firstprice)*100/firstprice:
        set_value("miny",(pastweek.min()-firstprice)*100/firstprice)
    print((pastweek.min()-firstprice)*100/firstprice,(pastweek.max()-firstprice)*100/firstprice)
    weeklist = []
    #make the price percent change from start
    for i in range(len(pastweek)):
        weeklist.append((i/(2709)*7,(pastweek[i]-firstprice)*100/firstprice))
    #print(weeklist)
    ''' 
    data1 = []
    for i in range(0, 100):
        data1.append([3.14 * i / 180, cos(3 * 3.14 * i / 180)])

    data2 = []
    for i in range(0, 100):
        data2.append([3.14 * i / 180, sin(2 * 3.14 * i / 180)])
    print(data2) 
    '''
    #use generator instead
    #iterate through list of colors
    newcolor = next(gen)
    print(newcolor)
    add_line_series("StockPlot", get_value('Stock Ticker'), weeklist, weight=2, fill=[newcolor[0],newcolor[1],newcolor[2], 100])
    #add_scatter_series("Plot", "test", weeklist)


start_dearpygui()
