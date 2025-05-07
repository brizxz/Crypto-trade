# backtester.py
from backtesting import Backtest
import pandas as pd

def run_backtest(data_df: pd.DataFrame, strategy_class, cash=100000, commission=0.001, plot_results=True):
    """
    運行回測並返回統計數據。

    參數:
    - data_df (pd.DataFrame): 包含 OHLCV 數據的 DataFrame，索引必須是 DatetimeIndex。
                              列名應為 'Open', 'High', 'Low', 'Close', 'Volume'。
    - strategy_class (Strategy): 要回測的策略類 (例如 MaCrossStrategy)。
    - cash (float): 初始資金。
    - commission (float): 手續費率 (例如 0.001 代表 0.1%)。
    - plot_results (bool): 是否繪製回測結果圖表。

    返回:
    - pd.Series: 回測的統計數據。如果出錯則返回 None。
    """
    if not isinstance(data_df.index, pd.DatetimeIndex):
        print("錯誤: 數據的索引必須是 DatetimeIndex。")
        try:
            # 嘗試轉換索引
            data_df.index = pd.to_datetime(data_df.index)
            print("已嘗試將索引轉換為 DatetimeIndex。")
        except Exception as e:
            print(f"轉換索引失敗: {e}")
            return None
            
    # 確保列名符合 backtesting.py 要求
    required_columns = ['Open', 'High', 'Low', 'Close'] # Volume 是可選的
    missing_columns = [col for col in required_columns if col not in data_df.columns]
    if missing_columns:
        print(f"錯誤: 數據 DataFrame 缺少以下必要列: {', '.join(missing_columns)}")
        return None
    
    if 'Volume' not in data_df.columns:
        print("警告: 數據 DataFrame 中缺少 'Volume' 列，將以0填充。")
        data_df['Volume'] = 0 # backtesting.py 需要 Volume 列，即使策略不用

    try:
        bt = Backtest(data_df, strategy_class, cash=cash, commission=commission, exclusive_orders=True)
        stats = bt.run()
        
        if plot_results:
            try:
                bt.plot()
            except Exception as e:
                print(f"繪製圖表時發生錯誤 (可能是由於缺少數據點或環境問題): {e}")
                print("回測統計數據仍會返回。")

        return stats
    except Exception as e:
        print(f"回測過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # 簡易測試 backtester.py (需要一個數據源和策略)
    # 創建一個簡單的 DataFrame 用於測試
    sample_data = { 
        'Open': [10, 11, 12, 11, 10, 11, 13, 14, 13, 12],
        'High': [11, 12, 13, 12, 11, 12, 14, 15, 14, 13],
        'Low': [9, 10, 11, 10, 9, 10, 12, 13, 12, 11],
        'Close': [11, 12, 11, 10, 11, 13, 14, 13, 12, 11],
        'Volume': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    }
    index = pd.to_datetime([f'2023-01-{i:02d}' for i in range(1, 11)])
    test_df = pd.DataFrame(sample_data, index=index)

    # 使用一個簡單的策略進行測試 (例如 MaCrossStrategy)
    from strategies.simple_ma_strategy import MaCrossStrategy
    
    print("正在運行 backtester.py 的簡易測試...")
    test_stats = run_backtest(test_df, MaCrossStrategy, cash=10000, commission=0.001, plot_results=False) # 設為False避免在無GUI環境下出錯
    
    if test_stats is not None:
        print("\nBacktester 測試統計:")
        print(test_stats)
    else:
        print("Backtester 測試失敗。")