import psycopg2
import twstock
import talib
import numpy as np
import matplotlib.pyplot as plt


def fetch_codes_from_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="Stock",
        user="postgres",
        password="123456"
    )
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT code FROM stock_data")
    codes = cur.fetchall()
    cur.close()
    conn.close()

    return [code[0] for code in codes]


def fetch_data_from_twstock(ticker):
    stock = twstock.Stock(ticker)
    data = stock.fetch_from(2023, 1)
    close = [d.close for d in data]
    volume = [d.capacity for d in data]
    dates = [d.date for d in data]
    return np.array(close), np.array(volume), dates


def calculate_vcp_conditions(close, volume):
    ema50 = talib.EMA(close, timeperiod=50)
    ema150 = talib.EMA(close, timeperiod=150)
    ema200 = talib.EMA(close, timeperiod=200)

    test = close[-1] >= ema50[-1] >= ema150[-1] >= ema200[-1] and np.all(np.diff(ema200[-31:]) > 0)

    return test, ema200, ema150, ema50


def plot_vcp(ticker, close, volume, dates, ema200, ema150, ema50):
    plt.figure(figsize=(14, 7))

    # 绘制收盘价和均线
    plt.subplot(2, 1, 1)
    plt.plot(dates, close, label='Close Price')
    plt.plot(dates, ema200, label='200-day EMA', color='red')
    plt.plot(dates, ema150, label='150-day EMA', color='orange')
    plt.plot(dates, ema50, label='50-day EMA', color='purple')
    plt.title(f'VCP Pattern for {ticker}')
    plt.ylabel('Price')
    plt.legend()

    # 绘制交易量
    plt.subplot(2, 1, 2)
    plt.bar(dates, volume, label='Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()

    plt.tight_layout()

    # 保存圖像
    plt.savefig(f'C:\AutoTrade\TaiwanStock\pic\{ticker}_vcp_pattern.png')

    plt.show()


def vcp_selection():
    codes = fetch_codes_from_db()
    selected_stocks = []

    for ticker in codes:
        print(ticker)
        close, volume, dates = fetch_data_from_twstock(ticker)
        condition, ema200, ema150, ema50 = calculate_vcp_conditions(close, volume)
        if condition:
            selected_stocks.append(ticker)
            plot_vcp(ticker, close, volume, dates, ema200, ema150, ema50)

    return selected_stocks


# 示例：筛选股票
selected_stocks = vcp_selection()
print("符合VCP的股票:", selected_stocks)
