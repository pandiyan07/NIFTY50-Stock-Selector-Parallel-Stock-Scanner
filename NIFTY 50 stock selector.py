from nselib import capital_market
from jugaad_data.nse import NSELive
import pandas as pd
import multiprocessing
import tracemalloc
import time
import sys
from datetime import datetime, timedelta

tracemalloc.start()


#-------Equity fetching block--------#
# below code fetches the nifty 50 equitly list symbols
NIFTY_50_stocks = capital_market.nifty50_equity_list()
eqList = ["INFY","ITC","WIPRO","TCS","ABB","RELIANCE","ICICI","SBIN"] #list(NIFTY_50_stocks["Symbol"])  
n = NSELive()
stock_data = {}


#-------Time Scheduling block--------#
# Set the target time (e.g., 8:30 AM)
target_start_hour, target_start_minute, target_start_second = 23, 37, 0
target_start_time = datetime.now().replace(hour=target_start_hour, minute=target_start_minute, second=target_start_second)

def RSI_CALCULATOR(close_prices):
    # Calculate price differences
    price_diffs = [close_prices[i] - close_prices[i - 1] for i in range(1, len(close_prices))]

    # Initialize lists for gains and losses
    gains = []
    losses = []

    # Separate gains and losses
    for diff in price_diffs:
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-diff)

    # Calculate average gains and losses over the 14-day period
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14

    # Calculate relative strength (RS)
    rs = avg_gain / avg_loss


    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi


def DMI_CALCULATOR(high, low, close, period):
    trs = []    # true range
    dms_pos = []
    dms_neg = []
    
    for i in range(1, len(close)):
        tr = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
        print (tr)
        
        """
        The max() function is then used to select the maximum value among these
        three differences,which represents the True Range for the current period.
        - high[i] - low[i] calculates the difference between the high price and the low price for the current period.
        - abs(high[i] - close[i-1]) calculates the absolute difference between the high price of the current period
        and the close price of the previous period.
        - abs(low[i] - close[i-1]) calculates the absolute difference between the low price of the current period and
        the close price of the previous period.
        - The abs() function ensures that the differences are positive, regardless of the order of subtraction.
        This is important for calculating the True Range accurately,
        as it measures the price movement regardless of direction.
        """
        trs.append(tr)
        print ("True range value :- ",trs)
        
        dm_pos = max(high[i] - high[i-1], 0)      # dm positive calculation
        """
        - The dm_pos variable stores the positive directional movement for a given period.
        
        - This line calculates the difference between the high price of the current period (high[i])
        and the high price of the previous period (high[i-1]).
        """
        print ("\n\nPositive DMS value :- ",dm_pos)
        dms_pos.append(dm_pos)
        dm_neg = max(low[i-1] - low[i], 0)        # dm negative calculation
        print ("Neagtive DMS value :- ",dm_neg)
        dms_neg.append(dm_neg)
    
    atr = sum(trs[-period:]) / period
    di_pos = sum(dms_pos[-period:]) / atr / period * 100
    di_neg = sum(dms_neg[-period:]) / atr / period * 100
    
    return di_pos, di_neg


def ADX_CALCULATOR(close, period):
    adx_values = []
    
    for i in range(period, len(close)):
        high = close[i-period:i]
        print ("The high value is : -",high)
        low = close[i-period:i]
        print ("The low value is : -",low)
        close_values = close[i-period:i]
        print ("The close value is : -",close)
        di_pos, di_neg = DMI_CALCULATOR(high, low, close_values, period)
        
        adx = abs(di_pos - di_neg) / (di_pos + di_neg) * 100  
        """
        calulating the ADX value using the DM positive & DM negative value
        
        In the provided code, the abs() function is used to calculate the absolute difference between two values.
        Specifically, it's used in the calculation of the True Range (tr).
        """
        adx_values.append(adx)
        print ("adx value is - ",adx)
        print ("Sum of ADX :- ",sum(adx_values))
        print ("Length of ADX :- ",len(adx_values))
        return sum(adx_values) / len(adx_values)



def FINAL_OUTPUT_DATAFRAME():
    data = {  
    "calories": [420,380,390],  
    "duration":[50,40,45]  
    }  
    df = pd.DataFrame(data, index = ["day1","day2","day3"])  
    print(df)


def DATA_FETCHER(start, end):  
    # give the Stock's symbol as input to this function & it will fetch the data for you
    """
    All the 50 processes should be enabled first.
    -- And they should be prepared for the 9:15am, then when 9:15am comes then all the processes should 
    """
    start_time = time.time()
    for i in range(start, end):
        q = n.stock_quote(eqList[i])
        individual_stock_data = {}
        
        # individual_stock_data["lastPrice"] = q['priceInfo']['lastPrice']
        individual_stock_data["pChange"] = q['priceInfo']['pChange']
        # individual_stock_data["previousClose"] = q['priceInfo']['previousClose']
        individual_stock_data["sector"] = q['industryInfo']['sector']
        individual_stock_data["basicIndustry"] = q['industryInfo']['basicIndustry']
        
        # Append values using update() method
        stock_data.update({eqList[i]:individual_stock_data})
        """
        for key,value in stock_data.items():
            print(f"{key}  =  {value}")
        """
        print(f"\nDATA FETCHER :- The current price of {eqList[i]} stock is = {stock_data[eqList[i]]['lastPrice']}")
    end_time = time.time()
    print(f"Data fetching completed in {end_time - start_time:.2f} seconds.")
    '''print ("The stocks are :-/n")
    for index, item in enumerate(eqList):
    print(f"{index}) {item}")'''
    
    
    # Calculating RSI value Example usage
    close_prices = [100, 102, 105, 103, 101, 98, 97, 99, 101, 100, 98, 96, 95, 97]
    rsi_value = RSI_CALCULATOR(close_prices)
    print(f"RSI value: {rsi_value:.2f}")
    
    # Calculating ADX value Example usage
    close_prices = [100, 102, 98, 105, 103, 107, 109, 110, 108, 106, 105, 107, 109, 112, 115]
    period = 14
    adx_value = ADX_CALCULATOR(close_prices, period)
    print("ADX value:", adx_value)



def SCHEDULE_TASK(start, end):
    while True:
        current_time = datetime.now()
        if current_time >= target_start_time:
            DATA_FETCHER(start, end)
            break
        print(current_time,' =======>>> ',target_start_time)
        time.sleep(1)

def WORKER_PROCESS_GENERATOR(num_of_process):
    # below main function code block fetches the price and other equity
    # datas for a specific number of stocks given as list inputs
    
    """Function to perform a task in parallel using multiprocessing."""
    i=0
    num_processor_cores = multiprocessing.cpu_count()
    print ("num_processor_cores :- ",num_processor_cores)
    print ("n :- ",num_of_process)
    chunk_size = num_of_process // num_processor_cores
    print ("chunk_size :- ",chunk_size)
    
    processes = []
    
    # This below for loop distributes the number of tasks among the 4 processes,
    # each process running on each of the device's core
    for i in range(num_processor_cores):
        start = i * chunk_size
        print ("\nstart :- ",start)
        end = start + chunk_size if i < num_processor_cores - 1 else num_of_process
        print ("end :- ",end,"\n")
        data_fetching_process = multiprocessing.Process(target=SCHEDULE_TASK, args=(start, end, ))
        print(data_fetching_process," HAS BEEN CREATED SUCCESFULLY...!!")
        print(f"Thread number {i+1} has been created successfully")
        processes.append(data_fetching_process)
        # setting start method as fork
        # multiprocessing.set_start_method('fork')  
        # #fork is not supported in Windows, as Windows & MacOS supports spawn only
        data_fetching_process.start()
        print ("-----------------------------------------------------------------------------------------------")
    
    
    '''
    print(f"\n{multiprocessing.get_start_method()}")
    print(f"\n{processes}\n")
    '''
    # Wait for all threads to finish
    for data_fetching_process in processes:
        print ("JOINING THE THREADSSS....................\n\n")
        data_fetching_process.join()
    
    for process in processes:
        print (process)
    




if __name__ == '__main__':
    # Call freeze_support() here
    multiprocessing.freeze_support()
    print ("\n\nThe server has started running...")
    
    # If the target time has already passed today, and print the message
    if target_start_time < datetime.now():
        #target_start_time += timedelta(days=1)      # schedule it for tomorrow
        print (f"Adangomma, the specified time {target_start_time} has already passed daa....!!")
        print ("exiting the program !!")
        sys.exit(1)  # Exit with a non-zero status (indicating an error)
    
    
    #---------------------Multiprocess block----------------------#
    
    print ("Bhaaaaiiiiiiii tera eqList lenghth :- ",len(eqList))
    WORKER_PROCESS_GENERATOR(len(eqList))
    
    """
    # Print each key-value pair on separate lines
    for key, value in q['priceInfo'].items():
        print(f"{key}: {value}")
    print (f"\n\n{q['priceInfo']['lastPrice']}\n{q['priceInfo']['pChange']}\n{q['priceInfo']['previousClose']}")
    """

    # Get the Total memory usage
    current_memory_usage = tracemalloc.get_traced_memory()[0]/(1024*1024)
    peak_memory_usage = tracemalloc.get_traced_memory()[1]/(1024*1024)
    # stopping the tracemalloc library
    tracemalloc.stop()

    print(f"\n\nCurrent Memory usage:- {current_memory_usage:.2f} MB")
    print(f"Peak Memory usage:- {peak_memory_usage:.2f} MB")