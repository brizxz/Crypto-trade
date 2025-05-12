# config.py

# API 金鑰設定 (請替換為您自己的金鑰)
# 注意：出於安全考量，不建議將API金鑰硬編碼在此處，尤其是在共享或版本控制的專案中。
# 考慮使用環境變數或安全的配置文件管理器。
API_KEY = ''  # 留空則表示使用公開API (如果交易所支持)
API_SECRET = '' # 留空則表示使用公開API

# 交易設定
EXCHANGE_ID = 'binance'  # 範例交易所，請根據您的選擇更改
TRADING_PAIR = 'BTC/USDT'
TIMEFRAME = '1d'  # K線週期: '1m', '5m', '15m', '1h', '4h', '1d', '1w', etc.

# 策略參數
STRATEGY_PARAMS = {
    'MA_Cross': {
        'n1': 10,  # 短期MA週期
        'n2': 20   # 長期MA週期
    },
    'RSI': {
        'rsi_period': 14,
        'overbought_threshold': 70,
        'oversold_threshold': 30
    }
    # 未來可以添加更多策略的參數
}

# 回測設定
BACKTEST_CONFIG = {
    'initial_cash': 100000,  # 初始資金
    'commission_rate': 0.001  # 手續費率 (例如 0.1%)
}

# 其他設定
LOG_LEVEL = 'INFO' # 日誌級別: DEBUG, INFO, WARNING, ERROR, CRITICAL
