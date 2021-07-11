# YOUR PROJECT TITLE
#### Video Demo:  "https://www.youtube.com/watch?v=YCENvsThKZ0"
#### Description:
This is a stock analyzer interface. There are four main pages: index, analyze, historical data and latest price.

## Index ##
The index page contains a button for the user to retrieve stock analytics. The analytics consist of three tables -- world indices, currencies (to HKD) and component stocks of Hang Sang Index. Three csv files are included for submission, which list the stock tickers in the three tables. Then, we download data using yfinance package. We calculate different stock indicators (volatility using Bollinger's Bands, stochastic oscillators, RSI, ADX) using talib. The Market Maturation index shows whether the market is oversold (<0) or overbought (>0), which is an adjusted mean of the stochastic oscillators and RSI. Latest stock prices and timestamps are also included. In such way, users can easily notice which stocks are oversold, overbought, or have strong and stable trends. 

## Analyze ##
In the "Analyze" page, users enter a stock symbol and the program output a series of analyzes. Error check is performed to ensure the symbols are included in yfinance tickers. Interative graph plotting is conducted using the plotly package. Candlestick plots are used for stock prices while other indicators are plotted using line graphs. Users can zoom in or out, or select the plots they want to visualize. Some simple interpretations are also given based on latest indicator values.

## Historical Data ##
In the "Historical Data" page, users enter a stock symbol, a start date, an end date and an interval values to extract historical data from yfinance API. Outputs are in the form of Candlestick graphs. 

## Latest Price ##
In the "Latest Price" page, users enter a stock symbol and the program returns a Candlestick graph of the stock prices of the latest day with minute-to-minute intervals.

## Special Note ##
This analyzer is specifically customized for users from HKSAR.
