# strategies/simple_ma_strategy.py
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA # backtesting.py 提供的 SMA 指標範例
# 或者，如果您想使用 TA-Lib 或 pandas-ta:
# import talib
# import pandas_ta as ta
# from config import STRATEGY_PARAMS # 如果參數在config中定義

# 從基類繼承 (可選)
from.base_strategy import BaseStrategy

class MaCrossStrategy(BaseStrategy): # 或直接 class MaCrossStrategy(Strategy):
    # 從 config.py 或直接定義策略參數
    # params = STRATEGY_PARAMS['MA_Cross']
    # n1 = params['n1']
    # n2 = params['n2']
    
    # 或者直接在類中定義參數，這樣可以在 Backtest.optimize 中優化
    n1 = 10  # 短期MA週期
    n2 = 20  # 長期MA週期

    def init(self):
        super().init() # 如果繼承自 BaseStrategy
        # 獲取收盤價數據
        close = self.data.Close
        
        # 計算短期MA
        # 使用 backtesting.py 內建的 SMA 範例
        self.sma1 = self.I(SMA, close, self.n1)
        
        # 計算長期MA
        self.sma2 = self.I(SMA, close, self.n2)

        # --- 如果使用 pandas-ta ---
        # self.data_df = self.data.to_df() # 轉換為DataFrame以便pandas-ta使用
        # self.data_df.ta.sma(length=self.n1, append=True, col_names=(f'SMA_{self.n1}',))
        # self.data_df.ta.sma(length=self.n2, append=True, col_names=(f'SMA_{self.n2}',))
        # self.sma1 = self.data_df
        # self.sma2 = self.data_df
        # --- 注意：使用pandas-ta直接修改self.data或創建新列需要小心處理與backtesting.py的集成 ---
        # --- 更推薦的方式是將pandas-ta的計算結果通過 self.I 封裝成指標 ---
        # def sma_indicator(series, length):
        #     return series.rolling(length).mean() # 簡單實現或調用pandas_ta
        # self.sma1 = self.I(sma_indicator, close, self.n1)
        # self.sma2 = self.I(sma_indicator, close, self.n2)


    def next(self):
        super().next() # 如果繼承自 BaseStrategy
        # 如果短期MA上穿長期MA
        if crossover(self.sma1, self.sma2):
            if not self.position:  # 如果沒有持倉，則買入
                self.buy()
            # 如果已有空頭倉位，則平倉後買入 (可選，取決於策略是否允許反轉)
            # elif self.position.is_short:
            #     self.position.close()
            #     self.buy()

        # 如果短期MA下穿長期MA
        elif crossover(self.sma2, self.sma1):
            if self.position.is_long:  # 如果持有多頭倉位，則賣出
                self.position.close() # 先平多倉
                # self.sell() # 然後開空倉 (如果策略允許做空)
            # 如果沒有持倉且允許做空，則直接開空倉 (可選)
            # elif not self.position and self.allow_shorting: # 假設有個 allow_shorting 參數
            #     self.sell()