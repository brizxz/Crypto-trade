# strategies/simple_rsi_strategy.py
from backtesting import Strategy
from backtesting.lib import crossover
# from config import STRATEGY_PARAMS # 如果參數在config中定義
from utils import rsi_indicator # 從 utils.py 導入RSI計算函數

# 從基類繼承 (可選)
from.base_strategy import BaseStrategy

class RsiStrategy(BaseStrategy): # 或直接 class RsiStrategy(Strategy):
    # params = STRATEGY_PARAMS
    # rsi_period = params['rsi_period']
    # overbought_threshold = params['overbought_threshold']
    # oversold_threshold = params['oversold_threshold']

    # 或者直接在類中定義參數，這樣可以在 Backtest.optimize 中優化
    rsi_period = 14
    overbought_threshold = 70
    oversold_threshold = 30

    def init(self):
        super().init() # 如果繼承自 BaseStrategy
        close = self.data.Close
        # 使用 self.I 註冊自定義的RSI指標 (rsi_indicator 來自 utils.py)
        self.rsi = self.I(rsi_indicator, close, self.rsi_period)

    def next(self):
        super().next() # 如果繼承自 BaseStrategy
        # 當前RSI值
        current_rsi = self.rsi[-1]

        # RSI 從下方上穿超賣線 - 買入信號
        if crossover(self.rsi, self.oversold_threshold):
            if not self.position: # 如果沒有持倉
                self.buy()
            # elif self.position.is_short: # 如果持有空倉，則平倉後買入 (反轉)
            #     self.position.close()
            #     self.buy()
        
        # RSI 從上方下穿超買線 - 賣出信號
        elif crossover(self.overbought_threshold, self.rsi): # 注意 crossover 的參數順序
            if self.position.is_long: # 如果持有多倉
                self.position.close() # 平多倉
                # self.sell() # 開空倉 (如果策略允許做空)
            # elif not self.position and self.allow_shorting: # 如果沒有持倉且允許做空
            #     self.sell()

        # 另一種常見的RSI邏輯：
        # 在超賣區 (RSI < 30) 且 RSI 開始回升時買入
        # if not self.position and current_rsi < self.oversold_threshold and self.rsi[-2] < current_rsi :
        #     self.buy()
        # 在超買區 (RSI > 70) 且 RSI 開始回落時賣出
        # elif self.position.is_long and current_rsi > self.overbought_threshold and self.rsi[-2] > current_rsi:
        #     self.position.close()