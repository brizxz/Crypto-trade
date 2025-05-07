# strategies/base_strategy.py
from backtesting import Strategy

class BaseStrategy(Strategy):
    """
    一個可選的策略基類，用於定義所有策略共有的通用接口或輔助方法。
    目前，它直接繼承自 backtesting.Strategy，沒有添加額外功能。
    您可以根據需要擴展它。
    """
    def init(self):
        super().init()
        # 可以在這裡添加所有策略都需要的通用初始化代碼
        # 例如，通用的日誌記錄設置

    def next(self):
        super().next()
        # 可以在這裡添加所有策略在每個時間步都可能執行的通用邏輯
        # 但通常具體的交易邏輯會在子類中實現

    def log(self, message):
        """一個簡單的日誌記錄輔助函數範例"""
        # 實際應用中，您可能會使用更完善的日誌庫 (如 logging)
        print(f"{self.data.index[-1]}: {message}")