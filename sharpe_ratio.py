import twstock
import pandas as pd
import numpy as np

# 获取台积电的历史数据（最近100天）
stock = twstock.Stock('3537')
data = pd.DataFrame({
    'date': stock.date[-100:],
    'close': stock.price[-100:]
})

# 打印数据进行验证
print(data.head())

# 计算每日收益率
data['Return'] = data['close'].pct_change()
print(data['Return'].head())

# 计算平均年化收益率
avg_daily_return = data['Return'].mean()
annualized_return = avg_daily_return * 252  # 年化收益率

# 计算收益率的年化标准差
daily_std_dev = data['Return'].std()
annualized_std_dev = daily_std_dev * np.sqrt(252)  # 年化标准差

# 打印验证计算的中间结果
print(f'平均年化收益率: {annualized_return}')
print(f'年化标准差: {annualized_std_dev}')

# 无风险利率（例如1.5%）
risk_free_rate = 0.015

# 计算夏普比率
sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std_dev
print(f'台积电过去100天的夏普比率为: {sharpe_ratio}')
