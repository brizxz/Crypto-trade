import pandas as pd
from config import API_KEY, API_SECRET, TRADING_PAIR, TIMEFRAME, STRATEGY_PARAMS, BACKTEST_CONFIG
from data_handler import fetch_ohlcv_data, load_data_from_csv
from strategies.simple_ma_strategy import MaCrossStrategy
from strategies.simple_rsi_strategy import RsiStrategy
from backtester import run_backtest
import os

def main():
    print("開始執行量化交易回測程式...")

    # 選擇數據來源：'api' 或 'csv'
    data_source = 'api'  # 或 'api'

    data_df = None

    if data_source == 'api':
        print(f"正在從 API ({TRADING_PAIR}, {TIMEFRAME}) 獲取數據...")
        # 注意：實際使用API獲取數據時，請確保config.py中的API金鑰已填寫
        # 且交易所支援無金鑰獲取公開數據，或已正確配置金鑰權限
        data_df = fetch_ohlcv_data(
            api_key=API_KEY,
            secret_key=API_SECRET,
            symbol=TRADING_PAIR,
            timeframe=TIMEFRAME,
            limit=500  # 可根據需求調整獲取數據的筆數
        )
    elif data_source == 'csv':
        # 確保 'data' 資料夾存在且包含指定的CSV檔案
        csv_file_path = os.path.join('data', 'btcusd_1d.csv') # 假設您有一個名為 btcusd_1d.csv 的檔案
        if not os.path.exists(csv_file_path):
            print(f"錯誤：找不到CSV檔案 {csv_file_path}")
            print("請將您的數據檔案放置在 'data' 資料夾下，或修改 'main.py' 中的檔案路徑。")
            print("您也可以從以下連結下載範例數據：https://www.cryptodatadownload.com/data/binance/")
            return

        print(f"正在從 CSV 檔案 ({csv_file_path}) 加載數據...")
        data_df = load_data_from_csv(csv_file_path)
        # 確保列名符合 backtesting.py 的要求 (Open, High, Low, Close, Volume)
        # CSV 檔案的日期欄位應設為索引 (parse_dates=True, index_col='Date' or 'Timestamp')
        # 例如:
        # data_df = pd.read_csv(csv_file_path, index_col='Date', parse_dates=True)
        # data_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume'] # 根據您的CSV調整


    if data_df is None or data_df.empty:
        print("數據獲取失敗，程式終止。")
        return

    print("數據加載完成。")
    print(data_df.head())

    # 選擇策略
    strategy_to_run = MaCrossStrategy
    # strategy_to_run = RsiStrategy
    print(f"選擇的策略: {strategy_to_run.__name__}")

    # 根據選擇的策略傳遞相應的參數
    if strategy_to_run == MaCrossStrategy:
        strategy_params = STRATEGY_PARAMS['MA_Cross']
        # MaCrossStrategy.n1 = strategy_params['n1'] # 可以在這裡動態設定，或在策略類中直接使用
        # MaCrossStrategy.n2 = strategy_params['n2']
    elif strategy_to_run == RsiStrategy:
        strategy_params = STRATEGY_PARAMS
        # RsiStrategy.rsi_period = strategy_params['rsi_period']
        # RsiStrategy.overbought_threshold = strategy_params['overbought_threshold']
        # RsiStrategy.oversold_threshold = strategy_params['oversold_threshold']
    else:
        print("未知的策略類型。")
        return

    print(f"策略參數: {strategy_params}")
    print("開始執行回測...")

    stats = run_backtest(
        data_df,
        strategy_to_run,
        cash=BACKTEST_CONFIG['initial_cash'],
        commission=BACKTEST_CONFIG['commission_rate']
    )

    if stats is not None:
        print("\n回測結果統計:")
        print(stats)
        # stats['_strategy'] 包含策略實例，可以訪問優化後的參數等
        # print("\n策略詳情:")
        # print(stats['_strategy'])
    else:
        print("回測執行出錯。")

    print("\n程式執行完畢。")

if __name__ == "__main__":
    main()