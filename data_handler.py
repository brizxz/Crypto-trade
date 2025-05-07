import ccxt
import pandas as pd
import os
def fetch_ohlcv_data(api_key=None, secret_key=None, symbol='BTC/USDT', timeframe='1d', limit=100, exchange_id='binance'):
    """
    使用 CCXT 從指定交易所獲取 OHLCV 數據。

    參數:
    - api_key (str, optional): API 金鑰。預設為 None。
    - secret_key (str, optional): API 密鑰。預設為 None。
    - symbol (str): 交易對，例如 'BTC/USDT'。預設為 'BTC/USDT'。
    - timeframe (str): K線週期，例如 '1d'。預設為 '1d'。
    - limit (int): 要獲取的數據點數量。預設為 100。
    - exchange_id (str): 交易所ID，例如 'binance'。預設為 'binance'。

    返回:
    - pandas.DataFrame: 包含 OHLCV 數據的 DataFrame，索引為時間戳。
                       列名為 ['Open', 'High', 'Low', 'Close', 'Volume']。
                       如果獲取失敗則返回 None。
    """
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange_params = {}
        if api_key and secret_key:
            exchange_params['apiKey'] = api_key
            exchange_params['secret'] = secret_key
        
        exchange = exchange_class(exchange_params)

        if not exchange.has['fetchOHLCV']:
            print(f"交易所 {exchange_id} 不支援 fetchOHLCV 功能。")
            return None

        print(f"正在從 {exchange_id} 獲取 {symbol} 的 {timeframe} K線數據，最近 {limit} 條...")
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        if not ohlcv:
            print("未能獲取到數據。")
            return None

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # 確保數據類型正確
        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Close'] = pd.to_numeric(df['Close'])
        df['Volume'] = pd.to_numeric(df['Volume'])

        print("數據獲取成功。")
        return df

    except ccxt.NetworkError as e:
        print(f"CCXT 網路錯誤: {e}")
        return None
    except ccxt.ExchangeError as e:
        print(f"CCXT 交易所錯誤: {e}")
        return None
    except Exception as e:
        print(f"獲取數據時發生未知錯誤: {e}")
        return None

def load_data_from_csv(file_path):
    """
    從 CSV 檔案加載 OHLCV 數據。
    CSV 檔案應包含 'Date' (或 'Timestamp'), 'Open', 'High', 'Low', 'Close', 'Volume' 列。
    'Date' (或 'Timestamp') 列應作為索引。
    """
    try:
        # 嘗試幾種常見的日期欄位名稱
        date_columns = ['Date', 'timestamp']
        df = None
        for col_name in date_columns:
            try:
                df_temp = pd.read_csv(file_path, index_col=col_name, parse_dates=True)
                # 檢查是否包含必要的 OHLCV 列 (大小寫不敏感)
                required_cols_lower = {'open', 'high', 'low', 'close', 'volume'}
                df_cols_lower = {col.lower() for col in df_temp.columns}
                if required_cols_lower.issubset(df_cols_lower):
                    df = df_temp
                    break
            except (ValueError, TypeError, KeyError):
                continue
        
        if df is None:
            print(f"錯誤：無法從 {file_path} 正確解析日期索引或找不到所有必要的OHLCV欄位。")
            print("請確保CSV檔案包含一個可解析的日期欄位作為索引，以及Open, High, Low, Close, Volume欄位。")
            return None

        # 標準化列名為 backtesting.py 所需的格式 (首字母大寫)
        column_mapping = {col.lower(): col for col in df.columns}
        rename_dict = {}
        for required_col_lower in ['open', 'high', 'low', 'close', 'volume']:
            original_col_name = None
            # 處理可能的列名大小寫問題
            if required_col_lower in column_mapping:
                 original_col_name = column_mapping[required_col_lower]
            elif required_col_lower.capitalize() in df.columns: # 如果已经是首字母大写
                 original_col_name = required_col_lower.capitalize()

            if original_col_name and original_col_name!= required_col_lower.capitalize():
                rename_dict[original_col_name] = required_col_lower.capitalize()
            elif not original_col_name:
                 # 如果找不到必要的列，則嘗試添加一個預設值（例如，如果Volume不存在）
                 if required_col_lower == 'volume' and 'Volume' not in df.columns:
                     print(f"警告：CSV檔案中未找到 'Volume' 列，將以0填充。")
                     df['Volume'] = 0
                 elif required_col_lower.capitalize() not in df.columns : # 如果連首字母大寫的都沒有
                     print(f"錯誤：CSV檔案中缺少必要的 '{required_col_lower.capitalize()}' 列。")
                     return None


        if rename_dict:
            df.rename(columns=rename_dict, inplace=True)
        
        # 確保列名是標準的 'Open', 'High', 'Low', 'Close', 'Volume'
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_cols:
            if col not in df.columns:
                if col == 'Volume': # 如果Volume不存在，給予預設值
                    print(f"警告：CSV檔案中未找到 '{col}' 列，將以0填充。")
                    df[col] = 0
                else:
                    print(f"錯誤：CSV檔案處理後仍缺少必要的 '{col}' 列。")
                    return None
        
        # 確保數據類型正確
        for col in expected_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.dropna(inplace=True) # 移除包含NaN的行，這些可能是由於類型轉換失敗造成的

        print(f"從 {file_path} 加載數據成功。")
        return df[expected_cols] # 只返回需要的列，並按指定順序

    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 {file_path}")
        return None
    except Exception as e:
        print(f"從 CSV 加載數據時發生錯誤: {e}")
        return None

if __name__ == '__main__':
    # 測試 fetch_ohlcv_data (需要有效的API金鑰或交易所支持公開訪問)
    # test_df_api = fetch_ohlcv_data(symbol='ETH/USDT', timeframe='1h', limit=10)
    # if test_df_api is not None:
    #     print("\nAPI 數據測試:")
    #     print(test_df_api.head())

    # 測試 load_data_from_csv (需要一個名為 sample_data.csv 的檔案在 data 資料夾中)
    # 創建一個範例CSV檔案用於測試
    sample_csv_path = 'data/sample_data.csv'
    os.makedirs('data', exist_ok=True)
    sample_data_content = """Date,Open,High,Low,Close,Volume
2023-01-01,16500,16600,16400,16550,1000
2023-01-02,16550,16700,16500,16650,1200
2023-01-03,16650,16680,16300,16400,1100
2023-01-04,16400,16800,16350,16750,1500
2023-01-05,16750,17000,16700,16950,1300
"""
    with open(sample_csv_path, 'w') as f:
        f.write(sample_data_content)
        
    test_df_csv = load_data_from_csv(sample_csv_path)
    if test_df_csv is not None:
        print("\nCSV 數據測試:")
        print(test_df_csv.head())
        print(test_df_csv.info())

    # 測試一個列名大小寫不同的CSV
    sample_csv_path_lower = 'data/sample_data_lower.csv'
    sample_data_content_lower = """timestamp,open,high,low,close,volume
2023-01-01,16500,16600,16400,16550,1000
2023-01-02,16550,16700,16500,16650,1200
"""
    with open(sample_csv_path_lower, 'w') as f:
        f.write(sample_data_content_lower)
    test_df_csv_lower = load_data_from_csv(sample_csv_path_lower)
    if test_df_csv_lower is not None:
        print("\nCSV (小寫列名) 數據測試:")
        print(test_df_csv_lower.head())
        print(test_df_csv_lower.info())