import twstock
import talib
import numpy as np
import psycopg2

def insert_stock(code, name, volume, last_price):
    """ 將股票數據插入 PostgreSQL 數據庫 """
    conn = psycopg2.connect(host='localhost', dbname='Stock', user='postgres', password='123456')
    cur = conn.cursor()
    print(conn)
    if conn:
        print("数据库连接成功!")
    cur.execute(
        """
        INSERT INTO stock_data (code, name, last_volume, last_price) 
        VALUES (%s, %s, %s, %s) 
        ON CONFLICT (code) 
        DO UPDATE SET 
            name = EXCLUDED.name, 
            last_volume = EXCLUDED.last_volume, 
            last_price = EXCLUDED.last_price
        """,
        (code, name, volume, last_price)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_stocks():
    stock_codes = twstock.codes

    for code, info in stock_codes.items():
        if info.type == '股票':
            stock = twstock.Stock(code)
            try:
                prices = stock.fetch_from(2014, 1)
                if prices[-1].transaction <= 1000:
                    continue
                if len(prices) < 2400:
                    continue
                close_prices = np.array([p.close for p in prices], dtype=float)
                ema50 = talib.EMA(close_prices, timeperiod=50)
                ema150 = talib.EMA(close_prices, timeperiod=150)
                ema200 = talib.EMA(close_prices, timeperiod=200)

                if (close_prices[-1] >= ema50[-1] >= ema150[-1] >= ema200[-1] and
                    np.all(np.diff(ema200[-31:]) > 0)):
                    last_price = close_prices[-1]
                    insert_stock(code, info.name, prices[-1].transaction, last_price)
            except Exception as e:
                print(f"Error processing {code}: {e}")

# 執行函數
get_stocks()
