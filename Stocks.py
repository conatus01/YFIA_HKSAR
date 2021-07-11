import csv
import math
import numpy as np
import pandas as pd
import yfinance as yf
import talib
import plotly.graph_objs as go
import plotly
import json
import sigfig

import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

#Overall analysis
#Individual analysis page
#Show figures on webpage
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
    
        with open('HKStocks.csv', newline='') as f:
            reader = csv.reader(f)
            dataS = list(reader)
        with open('HKCurrency.csv', newline='') as f:
            reader = csv.reader(f)
            dataC = list(reader)
        with open('Stockindex.csv', newline='') as f:
            reader = csv.reader(f)
            dataI = list(reader)

        DS1 = []
        DC1 = []
        DI1 = []
        DS2 = []
        DC2 = []
        DI2 = []
        hs = []
        hc = []
        hi =[]

        for i in range(len(dataS)):
            DS1.append(yf.download(tickers=dataS[i][0], period = "1y", interval = "1d"))
            DS2.append(yf.download(tickers=dataS[i][0], period = "1d", interval = "1m"))
            DS1[i].loc[:, 'upper'], DS1[i].loc[:, 'middle'], DS1[i].loc[:, 'lower'] = talib.BBANDS(DS1[i]['Close'])
            DS1[i].loc[:, 'band_width'] = DS1[i]['upper']-DS1[i]['lower']
            max_volatility = DS1[i]['band_width'][DS1[i]['band_width']==DS1[i]['band_width'].max()]
            if (len((DS1[i]['band_width'][-1] / max_volatility).values) == 1):
                volatility_indicator = (DS1[i]['band_width'][-1] / max_volatility).values[0]
            DS1[i].loc[:, 'RSI'] = talib.RSI(DS1[i]['Close'])
            RSI = DS1[i]['RSI'][-1]
            DS1[i].loc[:, '14-high'] = DS1[i].High.rolling(14).max()
            DS1[i].loc[:, '14-low'] = DS1[i].Low.rolling(14).min()
            DS1[i].loc[:, '%K'] = (DS1[i]['Close'] - DS1[i]['14-low'])*100/(DS1[i]['14-high'] - DS1[i]['14-low'])
            DS1[i].loc[:, '%D'] = DS1[i]['%K'].rolling(3).mean()
            SO = DS1[i]['%D'][-1]
            DS1[i].loc[:, 'ADX'] = talib.ADX(DS1[i]['High'], DS1[i]['Low'], DS1[i]['Close'], timeperiod=14)
            adx = DS1[i]['ADX'][-1]
            lp = DS2[i]['Close'][-1]
            msi  = ((RSI+SO) / 100)-1

            hs.append({"Symbol": dataS[i][0], "Last price": str(np.round(lp,3)), "volat": str(np.round(volatility_indicator,3)), "SO": str(np.round(SO,1)), "RSI": str(np.round(RSI,1)), "MSI": np.round(msi,3), "ADX": np.round(adx,1), "Last update": DS2[i].index[-1]})


        print(hs)
        for i in range(len(dataC)):
            DC1.append(yf.download(tickers=dataC[i][0], period = "1y", interval = "1d"))
            DC2.append(yf.download(tickers=dataC[i][0], period = "1d", interval = "1m"))
            DC1[i].loc[:, 'upper'], DC1[i].loc[:, 'middle'], DC1[i].loc[:, 'lower'] = talib.BBANDS(DC1[i]['Close'])
            DC1[i].loc[:, 'band_width'] = DC1[i]['upper']-DC1[i]['lower']
            max_volatility = DC1[i]['band_width'][DC1[i]['band_width']==DC1[i]['band_width'].max()]
            if (len((DC1[i]['band_width'][-1] / max_volatility).values) == 1):
                volatility_indicator = (DC1[i]['band_width'][-1] / max_volatility).values[0]
            DC1[i].loc[:, 'RSI'] = talib.RSI(DC1[i]['Close'])
            RSI = DC1[i]['RSI'][-1]
            DC1[i].loc[:, '14-high'] = DC1[i].High.rolling(14).max()
            DC1[i].loc[:, '14-low'] = DC1[i].Low.rolling(14).min()
            DC1[i].loc[:, '%K'] = (DC1[i]['Close'] - DC1[i]['14-low'])*100/(DC1[i]['14-high'] - DC1[i]['14-low'])
            DC1[i].loc[:, '%D'] = DC1[i]['%K'].rolling(3).mean()
            SO = DC1[i]['%D'][-1]
            DC1[i].loc[:, 'ADX'] = talib.ADX(DC1[i]['High'], DC1[i]['Low'], DC1[i]['Close'], timeperiod=14)
            adx = DC1[i]['ADX'][-1]
            lp = DC2[i]['Close'][-1]
            msi  = ((RSI+SO) / 100)-1

            hc.append({"Symbol": dataC[i][0], "Last price": str(np.round(lp,3)), "volat": str(np.round(volatility_indicator,3)), "SO": str(np.round(SO,1)), "RSI": str(np.round(RSI,1)), "MSI": np.round(msi,3), "ADX": np.round(adx,1), "Last update": DC2[i].index[-1]})    
        print(hc)

        for i in range(len(dataI)):
            DI1.append(yf.download(tickers=dataI[i][0], period = "1y", interval = "1d"))
            DI2.append(yf.download(tickers=dataI[i][0], period = "1d", interval = "1m"))
            DI1[i].loc[:, 'upper'], DI1[i].loc[:, 'middle'], DI1[i].loc[:, 'lower'] = talib.BBANDS(DI1[i]['Close'])
            DI1[i].loc[:, 'band_width'] = DI1[i]['upper']-DI1[i]['lower']
            max_volatility = DI1[i]['band_width'][DI1[i]['band_width']==DI1[i]['band_width'].max()]
            if (len((DI1[i]['band_width'][-1] / max_volatility).values) == 1):
                volatility_indicator = (DI1[i]['band_width'][-1] / max_volatility).values[0]
            DI1[i].loc[:, 'RSI'] = talib.RSI(DI1[i]['Close'])
            RSI = DI1[i]['RSI'][-1]
            DI1[i].loc[:, '14-high'] = DI1[i].High.rolling(14).max()
            DI1[i].loc[:, '14-low'] = DI1[i].Low.rolling(14).min()
            DI1[i].loc[:, '%K'] = (DI1[i]['Close'] - DI1[i]['14-low'])*100/(DI1[i]['14-high'] - DI1[i]['14-low'])
            DI1[i].loc[:, '%D'] = DI1[i]['%K'].rolling(3).mean()
            SO = DI1[i]['%D'][-1]
            DI1[i].loc[:, 'ADX'] = talib.ADX(DI1[i]['High'], DI1[i]['Low'], DI1[i]['Close'], timeperiod=14)
            adx = DI1[i]['ADX'][-1]
            lp = DI2[i]['Close'][-1]
            msi  = ((RSI+SO) / 100)-1

            hi.append({"Symbol": dataI[i][0], "Last price": str(np.round(lp,3)), "volat": str(np.round(volatility_indicator,3)), "SO": str(np.round(SO,1)), "RSI": str(np.round(RSI,1)), "MSI": np.round(msi,3), "ADX": np.round(adx,1), "Last update": DI2[i].index[-1]})   

        return render_template('main.html',hs=hs, hc=hc, hi=hi)
    else:
        return render_template("welcome.html")


@app.route('/Analyze', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        code = request.form.get("symbol").upper()
        ticker = yf.Ticker(code)
        if ticker.info['regularMarketPrice'] is None:
            return render_template("invalid.html")

        data = yf.download(tickers=code, period = "1y", interval = "1d")

        data.loc[:, 'ma10'] = data.Close.rolling(10).mean()
        data.loc[:, 'ma20'] = data.Close.rolling(20).mean()
        data.loc[:, 'ma50'] = data.Close.rolling(50).mean()
        data.loc[:, 'ma100'] = data.Close.rolling(100).mean()
        data.loc[:, 'ma200'] = data.Close.rolling(200).mean()
        data.loc[:, 'ema12'] = data.Close.ewm(span=12, adjust=False).mean()
        data.loc[:, 'ema26'] = data.Close.ewm(span=26, adjust=False).mean()
        data.loc[:, 'ema50'] = data.Close.ewm(span=50, adjust=False).mean()
        data.loc[:, 'ema200'] = data.Close.ewm(span=200, adjust=False).mean()
        data.loc[:, 'macd'], data.loc[:,'macd_signal'], data.loc[:, 'macd_hist'] = talib.MACD(data['Close'])
        data.loc[:, 'upper'], data.loc[:, 'middle'], data.loc[:, 'lower'] = talib.BBANDS(data['Close'])
        data.loc[:, 'band_width'] = data['upper']-data['lower']


        #Construct requested price figure
        truncated_title = ''
        truncated_title_1 = '<b>Stock prices, moving averages, EMA, Bollinger Bands</b>'
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='market data'))

        #Add moving averages, EMA and Bollinger Bands according to the number of intervals (at least 4x)
        if (len(data) > 40):
            fig.add_trace(go.Scatter(x=data.index, y=data['ma10'], name='ma10', line=dict(width=1)))
            if (len(data) >48):
                fig.add_trace(go.Scatter(x=data.index, y=data['ema12'], name='ema12', line=dict(width=1)))
                if (len(data) > 80):
                    fig.add_trace(go.Scatter(x=data.index, y=data['ma20'], name='ma20', line=dict(width=1)))
                    if (len(data) > 104):
                        fig.add_trace(go.Scatter(x=data.index, y=data['ema26'], name='ema26', line=dict(width=1)))
                        if (len(data) > 200):
                            fig.add_trace(go.Scatter(x=data.index, y=data['ma50'], name='ma50', line=dict(width=1)))
                            fig.add_trace(go.Scatter(x=data.index, y=data['ema50'], name='ema50', line=dict(width=1)))
                            if (len(data) > 400):
                                fig.add_trace(go.Scatter(x=data.index, y=data['ma100'], name='ma100', line=dict(width=1)))
                                if (len(data) > 800):
                                    fig.add_trace(go.Scatter(x=data.index, y=data['ma200'], name='ma200', line=dict(width=1)))
                                    fig.add_trace(go.Scatter(x=data.index, y=data['ema200'], name='ema200', line=dict(width=1)))
        fig.add_trace(go.Scatter(x=data.index, y=data['upper'], name='upper Bollinger band', line=dict(width=1, dash ='dot')))
        fig.add_trace(go.Scatter(x=data.index, y=data['lower'], name='lower Bollinger band', line=dict(width=1, dash ='dot')))
        fig.update_layout(title=truncated_title_1, yaxis_title='Stock Price')
        fig.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig.update_yaxes(autorange=True, fixedrange=False)

        #Add basic interpretation on Bollinger's Bands
        txt00= "Latest Bollinger's bands recorded at "+str(data.index[-1])+" is <b>"+str(data['lower'][-1])+"</b> to <b>"+str(data['upper'][-1])+".</b>"
        max_volatility = data['band_width'][data['band_width']==data['band_width'].max()]
        volatility_indicator = (data['band_width'][-1] / max_volatility).values
        txt01= "Volatility indicator (ranges from 0 to 1) is: <b>"+str(round(volatility_indicator[0],3))+".</b>"
        fig.add_annotation(dict(font=dict(size=14), x=0, y=-0.6,showarrow=False, text=txt00, textangle=0, xanchor='left', xref="paper", yref="paper"))
        fig.add_annotation(dict(font=dict(size=14), x=0, y=-0.68,showarrow=False, text=txt01, textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['Close'][-1] <data['lower'][-1]):
            fig.add_annotation(dict(font=dict(size=14, color='red'),  x=1, y=-0.68,showarrow=False, text="<b>Market oversold.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if ((data['Close'][-1] >=data['lower'][-1]) and (data['Close'][-1] <= data['upper'][-1])):
            fig.add_annotation(dict(font=dict(size=14, color='green'),  x=1, y=-0.68,showarrow=False, text="<b>Market normal.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['Close'][-1] >data['upper'][-1]):
            fig.add_annotation(dict(font=dict(size=14, color='red'),  x=1, y=-0.68,showarrow=False, text="<b>Market overbought.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))

        #Stochastic oscillator
        data.loc[:, '14-high'] = data.High.rolling(14).max()
        data.loc[:, '14-low'] = data.Low.rolling(14).min()
        data.loc[:, '%K'] = (data['Close'] - data['14-low'])*100/(data['14-high'] - data['14-low'])
        data.loc[:, '%D'] = data['%K'].rolling(3).mean()

        #Plot stochastic oscillator on a separate graph
        truncated_title_2 = truncated_title + "<b>Stochastic Oscillators</b>"
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=data.index, y=data['%K'], name='Stochastic oscillator (raw)', line = dict(width = 2)))
        fig2.add_trace(go.Scatter(x=data.index, y=data['%D'], name='Stochastic oscillator (moving average)', line = dict(width = 2)))
        fig2.update_layout(title=truncated_title_2, yaxis_title='Stochastic oscillator')
        fig2.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig2.update_yaxes(autorange=True, fixedrange=False)

        #Add basic interpretations
        txt1= "Latest stochastic oscillator (raw) recorded at "+str(data.index[-1])+" is <b>"+str(round(data['%K'][-1],1))+".</b>"
        txt2= "Latest stochastic oscillator (moving average) recorded at "+str(data.index[-1])+" is <b>"+str(round(data['%D'][-1],1))+".</b>"

        fig2.add_annotation(dict(font=dict(size=14), x=0, y=-0.6,showarrow=False, text=txt1, textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['%K'][-1] <20):
            fig2.add_annotation(dict(font=dict(size=14, color='red'),  x=1.1, y=-0.6,showarrow=False, text="<b>Market oversold.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if ((data['%K'][-1] >=20) and (data['%K'][-1] <=80)):
            fig2.add_annotation(dict(font=dict(size=14, color='green'),  x=1.1, y=-0.6,showarrow=False, text="<b>Market normal.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['%K'][-1] >80):
            fig2.add_annotation(dict(font=dict(size=14, color='red'),  x=1.1, y=-0.6,showarrow=False, text="<b>Market overbought.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))

    
        fig2.add_annotation(dict(font=dict(size=14), x=0, y=-0.68,showarrow=False, text=txt2, textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['%D'][-1] <20):
            fig2.add_annotation(dict(font=dict(size=14, color='red'),  x=1.1, y=-0.68,showarrow=False, text="<b>Market oversold.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if ((data['%D'][-1] >=20) and (data['%D'][-1] <=80)):
            fig2.add_annotation(dict(font=dict(size=14, color='green'),  x=1.1, y=-0.68,showarrow=False, text="<b>Market normal.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['%D'][-1] >80):
            fig2.add_annotation(dict(font=dict(size=14, color='red'),  x=1.1, y=-0.68,showarrow=False, text="<b>Market overbought.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))


        #Plot MACD
        truncated_title_3 = truncated_title + "<b>MACD</b>"
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=data.index, y=data['macd'], name='macd', line = dict(width = 1)))
        fig3.add_trace(go.Scatter(x=data.index, y=data['macd_signal'], name='macd_signal', line = dict(width = 1)))
        fig3.add_trace(go.Bar(x=data.index, y=data['macd_hist'], name='macd_hist'))
        fig3.update_layout(title=truncated_title_3, yaxis_title='MACD')
        fig3.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig3.update_yaxes(autorange=True, fixedrange=False)

        #Plot RSI
        data.loc[:, 'RSI'] = talib.RSI(data['Close'])
        truncated_title_4 = truncated_title + "<b>RSI</b>"
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line = dict(width = 1)))
        fig4.update_layout(title=truncated_title_4, yaxis_title='RSI')
        fig4.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig4.update_yaxes(autorange=True, fixedrange=False)

        #Add RSI interpretations
        txt3= "Latest relative strength index (RSI) recorded at "+str(data.index[-1])+" is <b>"+str(round(data['RSI'][-1],1))+".</b>"
        fig4.add_annotation(dict(font=dict(size=14), x=0, y=-0.6,showarrow=False, text=txt3, textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['RSI'][-1] <30):
            fig4.add_annotation(dict(font=dict(size=14, color='red'),  x=0.9, y=-0.6,showarrow=False, text="<b>Market oversold.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if ((data['RSI'][-1] >=30) and (data['RSI'][-1] <=70)):
            fig4.add_annotation(dict(font=dict(size=14, color='green'),  x=0.9, y=-0.6,showarrow=False, text="<b>Market normal.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['RSI'][-1] >70):
            fig4.add_annotation(dict(font=dict(size=14, color='red'),  x=0.9, y=-0.6,showarrow=False, text="<b>Market overbought.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))

        #Plot average directional index (ADX)
        data.loc[:, 'ADX'] = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=14)
        truncated_title_5 = truncated_title + "<b>ADX</b>"
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=data.index, y=data['ADX'], name='ADX', line = dict(width = 1)))
        fig5.update_layout(title=truncated_title_5, yaxis_title='ADX')
        fig5.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig5.update_yaxes(autorange=True, fixedrange=False)

        #Add ADX interpretations
        txt4= "Latest average directional index (ADX) recorded at "+str(data.index[-1])+" is <b>"+str(round(data['ADX'][-1],1))+".</b>"
        fig5.add_annotation(dict(font=dict(size=14), x=0, y=-0.6,showarrow=False, text=txt4, textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['ADX'][-1] <=25):
            fig5.add_annotation(dict(font=dict(size=14, color='red'),  x=0.8, y=-0.6,showarrow=False, text="<b>Absent or weak trend.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if ((data['ADX'][-1] >25) and (data['ADX'][-1] <=50)):
            fig5.add_annotation(dict(font=dict(size=14, color='lightgreen'),  x=0.8, y=-0.6,showarrow=False, text="<b>Strong trend.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if ((data['ADX'][-1] >50) and (data['ADX'][-1] <=75)):
            fig5.add_annotation(dict(font=dict(size=14, color='green'),  x=0.8, y=-0.6,showarrow=False, text="<b>Very strong trend.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))
        if (data['ADX'][-1] >75):
            fig5.add_annotation(dict(font=dict(size=14, color='darkgreen'),  x=0.8, y=-0.6,showarrow=False, text="<b>Extremely strong trend.</b>", textangle=0, xanchor='left', xref="paper", yref="paper"))

        graphJSON1=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('analyzed.html', graphJSON1=graphJSON1, graphJSON2=graphJSON2, graphJSON3=graphJSON3, graphJSON4=graphJSON4, graphJSON5=graphJSON5, code=code)
    else:
        return render_template('analyze.html')

@app.route('/History', methods=["GET", "POST"])
def history():

    if request.method == "POST":
        a = ((not request.form.get("symbol")) or (not request.form.get("start")) or (not request.form.get("end")) or (not request.form.get("interval")))
        ss = request.form.get("start")
        ee = request.form.get("end")
        ii = request.form.get("interval")
        if (a):
            return a
        else:
            code = request.form.get("symbol").upper()
            ticker = yf.Ticker(code)
            if ticker.info['regularMarketPrice'] is None:
                return render_template("invalid.html")
        data = yf.download(tickers=code, start = request.form.get("start"), end = request.form.get("end"), interval = request.form.get("interval"))

        #Construct requested price figure
        truncated_title = ''
        truncated_title_1 = '<b>Stock prices from '+request.form.get("start")+' to '+request.form.get("end")+'.</b>'
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='market data'))
        fig.update_layout(title=truncated_title_1, yaxis_title='Stock Price')
        fig.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig.update_yaxes(autorange=True, fixedrange=False)
        graphJSON1=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('historydata.html', graphJSON1=graphJSON1, code=code, ss=ss, ee=ee, ii=ii)
    else:
        return render_template('history.html')

@app.route('/Latest', methods=["GET", "POST"])
def latest():
    if request.method == "POST":
        code = request.form.get("symbol").upper()
        ticker = yf.Ticker(code)
        if ticker.info['regularMarketPrice'] is None:
            return render_template("invalid.html")

        data = yf.download(tickers=code, period = "1d", interval = "1m")
        
        lp = str(data['Close'][-1])
        tm = str(data.index[-1])

        #Construct requested price figure
        truncated_title = ''
        truncated_title_1 = ''
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='market data'))
        fig.update_layout(title=truncated_title_1, yaxis_title='Stock Price')
        fig.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=15, label='15m', step='minute', stepmode='backward'),
                    dict(count=1, label='1h', step='hour', stepmode='backward'),
                    dict(count=2, label='2h', step='hour', stepmode='backward'),
                    dict(count=6, label='6h', step='hour', stepmode='backward'),
                    dict(count=12, label='12h', step='hour', stepmode='backward'),
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=2, label='2d', step='day', stepmode='backward'),
                    dict(count=5, label='5d', step='day', stepmode='backward'),
                    dict(count=10, label='10d', step='day', stepmode='backward'),
                    dict(count=1, label='1mo', step='month', stepmode='backward'),
                    dict(count=3, label='3mo', step='month', stepmode='backward'),
                    dict(count=6, label='6mo', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(count=2, label='2y', step='year', stepmode='backward'),
                    dict(count=5, label='5y', step='year', stepmode='backward'),
                    dict(count=10, label='10y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        fig.update_yaxes(autorange=True, fixedrange=False)
        graphJSON1=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template("latestdata.html", graphJSON1=graphJSON1, lp=lp, tm=tm, code=code)
    else:
        return render_template("latest.html")


if __name__ == "__main__":
    app.run()
