# utils.py
import pandas as pd
# import logging # 如果需要更複雜的日誌記錄

# def setup_logging(level='INFO'):
#     """配置基本的日誌記錄器。"""
#     logging.basicConfig(level=level,
#                         format='%(asctime)s - %(levelname)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')

def rsi_indicator(series: pd.Series, n: int = 14) -> pd.Series:
    """
    計算相對強弱指數 (RSI)。
    這是 backtesting.py 文件中常見的RSI實現方式，用於 self.I()。

    參數:
    - series (pd.Series): 收盤價序列。
    - n (int): RSI的計算週期，預設為14。

    返回:
    - pd.Series: RSI 值序列。
    """
    # Ensure series is a pandas Series
    if not isinstance(series, pd.Series):
        series = pd.Series(series)
        
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
    
    # 避免除以零
    # 當 loss 為 0 時，如果 gain 也為 0，則 RS 為 1 (RSI=50)
    # 如果 gain > 0 且 loss = 0, RS 趨近於無窮大 (RSI=100)
    rs = gain / loss
    rs = rs.replace([float('inf'), -float('inf')], 1000) # 用一個大數代替無窮大
    rs = rs.fillna(1) # 處理初始的NaN值，假設初始RS為1 (RSI=50)

    rsi = 100 - (100 / (1 + rs))
    return rsi

if __name__ == '__main__':
    # 測試 RSI 指標函數
    data = {'Close': [10, 12, 11, 13, 15, 14, 16, 17, 18, 15, 14, 13, 15, 17, 19, 20, 18, 17]}
    df = pd.DataFrame(data)
    
    rsi_values = rsi_indicator(df['Close'], n=5) # 使用較小的n值以便觀察
    print("RSI 測試值:")
    print(rsi_values)