# Project Title

**NIFTY 50 Stock Selector & Parallel Market Scanner**

Built on - May 2024

## Table of Contents

-   [About The Project](#about-the-project)
-   [Built With](#built-with)
-   [Key Features](#key-features)
-   [Getting Started](#getting-started)
-   [Technologies Used
    (Prerequisites)](#technologies-used-prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Project Structure](#project-structure)
-   [How It Works](#how-it-works)
-   [Main Python Functions](#main-python-functions)
-   [Future Improvements](#future-improvements)
-   [License Description](#license-description)
-   [Disclaimer](#disclaimer)

## About The Project

This project is a multiprocessing-based stock scanner for the Indian
stock market. It retrieves NIFTY 50 stocks (or a custom watchlist),
schedules execution at a predefined market time, fetches live market
data from NSE, computes basic technical indicators (RSI, DMI and ADX),
monitors memory usage, and demonstrates parallel data collection for
multiple equities.

### Built With

-   Python 3
-   nselib
-   jugaad-data
-   pandas
-   multiprocessing
-   tracemalloc
-   datetime
-   time
-   sys

### Key Features

-   Fetches NIFTY 50 symbols
-   Live NSE quote retrieval
-   Scheduled execution
-   Multiprocessing worker allocation
-   RSI calculation
-   DMI calculation
-   ADX calculation
-   Memory profiling
-   Sector and industry extraction
-   Modular function-based design

## Getting Started

### Technologies Used (Prerequisites)

-   Python 3.10+
-   Internet connection
-   NSE access
-   `pip`

Required packages:

``` bash
pip install pandas nselib jugaad-data
```

### Installation

``` bash
git clone https://github.com/pandiyan07/NIFTY50-Stock-Selector-Parallel-Stock-Scanner.git
cd NIFTY50-Stock-Selector-Parallel-Stock-Scanner
pip install -r requirements.txt
python "NIFTY 50 stock selector.py"
```

## Usage

Run the script before market open, configure the target execution time,
define the watchlist (or use the NIFTY 50 list), and execute the
program. Worker processes automatically start at the scheduled time and
fetch live stock information.

## Project Structure

``` text
NIFTY 50 stock selector.py
│
├── Configuration
│   ├── Watchlist
│   ├── Scheduler
│   └── Global storage
│
├── RSI_CALCULATOR()
├── DMI_CALCULATOR()
├── ADX_CALCULATOR()
├── DATA_FETCHER()
├── SCHEDULE_TASK()
├── WORKER_PROCESS_GENERATOR()
└── Main Program
```

## How It Works

1.  Initialize libraries and global variables.
2.  Load the NIFTY 50 list or custom symbols.
3.  Configure the scheduled execution time.
4.  Create multiprocessing workers.
5.  Wait until the target time.
6.  Fetch live stock quotes from NSE.
7.  Extract sector and industry information.
8.  Calculate RSI.
9.  Calculate DMI.
10. Calculate ADX.
11. Store results in dictionaries.
12. Display runtime and memory statistics.

## Main Python Functions

  -----------------------------------------------------------------------
  Function                       Description
  ------------------------------ ----------------------------------------
  `RSI_CALCULATOR()`             Calculates Relative Strength Index from
                                 closing prices.

  `DMI_CALCULATOR()`             Computes positive and negative
                                 Directional Movement values.

  `ADX_CALCULATOR()`             Calculates Average Directional Index
                                 using DMI values.

  `DATA_FETCHER()`               Downloads live stock information and
                                 triggers indicator calculations.

  `SCHEDULE_TASK()`              Waits until the configured execution
                                 time before running data collection.

  `WORKER_PROCESS_GENERATOR()`   Creates and manages multiprocessing
                                 workers across CPU cores.

  `FINAL_OUTPUT_DATAFRAME()`     Demonstration function for DataFrame
                                 creation.
  -----------------------------------------------------------------------

## Future Improvements

-   Rank stocks by relative strength.
-   Add EMA, MACD and Bollinger Bands.
-   Export results to CSV/Excel.
-   Real-time dashboard.
-   Alert notifications.
-   Volume and momentum filters.

## License Description

Recommended License: MIT License.

Permission is granted to use, modify, distribute and commercialize the
software while preserving the original copyright notice and license
text.

## Disclaimer

This project is intended for educational and research purposes only. It
is not financial advice. Verify all trading decisions independently
before using them in live markets.
