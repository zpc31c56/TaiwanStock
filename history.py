import twstock
import talib
import numpy as np

# 確保TA-Lib和twstock已經安裝
def get_rsi_under_30_stocks():
    stock_codes = twstock.codes  # 取得所有股票代碼
    stocks_under_rsi_30 = []  # 儲存RSI低於30的股票

    for code, info in stock_codes.items():
        if info.type == '股票':  # 確保只查詢股票，排除其他金融商品
            stock = twstock.Stock(code)
            try:
                prices = stock.fetch_from(2024, 4)  # 示例：抓取2023年1月的數據
                print(prices)
                close_prices = np.array([p.close for p in prices], dtype=float)
                rsi = talib.RSI(close_prices, timeperiod=14)  # 計算14天RSI
                if len(rsi) > 0 and rsi[-1] < 30:  # 檢查最新的RSI值
                    stocks_under_rsi_30.append((code, info.name, rsi[-1]))
            except Exception as e:
                print(f"Error processing {code}: {e}")

    return stocks_under_rsi_30

# 執行函數並打印結果
result = get_rsi_under_30_stocks()
for item in result:
    print(f"股票代碼: {item[0]}, 名稱: {item[1]}, RSI: {item[2]:.2f}")
