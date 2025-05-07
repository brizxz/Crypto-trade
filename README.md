## 功能

*   **數據獲取**: 支持通過 CCXT 從交易所 API 獲取歷史 K 線數據，或從本地 CSV 檔案加載數據。
*   **策略實現**: 內建了兩種簡單的交易策略範例：
    *   移動平均線 (MA) 交叉策略
    *   相對強弱指數 (RSI) 策略
*   **回測系統**: 使用 `backtesting.py` 函式庫執行交易策略的回測。
*   **績效評估**: 輸出回測的關鍵績效指標，如總回報率、夏普比率、最大回撤等。
*   **可配置性**: 通過 `config.py` 檔案管理 API 金鑰、策略參數和回測設定。

## 安裝

1.  **克隆專案** (如果您是從版本控制系統獲取):
    ```bash
    git clone <repository_url>
    cd crypto_quant_project
    ```

2.  **創建並激活虛擬環境** (推薦):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **安裝依賴**:
    ```bash
    pip install -r requirements.txt
    ```
    *注意*: 如果 `TA-Lib` 安裝困難，您可以考慮從 `requirements.txt` 中移除它 (如果策略未使用)，或者查找適合您作業系統的安裝指南。`pandas-ta` 通常是更容易安裝的替代品。

## 使用方法

1.  **配置 `config.py`**:
    *   如果您打算使用 API 獲取數據，請在 `config.py` 中填寫您的 `API_KEY` 和 `API_SECRET`。
    *   根據需要調整 `TRADING_PAIR`, `TIMEFRAME` 以及策略參數和回測設定。

2.  **準備數據** (如果使用 CSV):
    *   將您的 CSV 數據檔案放入 `data/` 資料夾中。
    *   確保 CSV 檔案的格式 (日期索引，列名如 Open, High, Low, Close, Volume) 與 `data_handler.py` 中的 `load_data_from_csv` 函數兼容。
    *   修改 `main.py` 中的 `data_source` 變數為 `'csv'`，並確保 `csv_file_path` 指向正確的檔案。

3.  **運行主程式**:
    ```bash
    python main.py
    ```
    程式將根據您的配置加載數據，執行選定的策略回測，並打印結果統計。如果 `plot_results` 為 `True` (在 `backtester.py` 的 `run_backtest` 函數中)，則會嘗試顯示回測圖表。

## 注意事項

*   **API 金鑰安全**: 切勿將包含真實 API 金鑰的 `config.py` 文件提交到公開的版本控制庫。考慮使用環境變數或其他安全方式管理敏感信息。
*   **數據質量**: 回測結果的可靠性高度依賴於歷史數據的質量。請確保使用準確且經過清洗的數據。
*   **過度優化**: 避免過度優化策略參數以適應歷史數據，這可能導致策略在未來實際市場中表現不佳。
*   **風險提示**: 量化交易涉及風險，歷史回測績效不代表未來收益。本專案僅為教學和研究目的。

## 未來擴展

*   實現更多複雜的交易策略。
*   集成更高級的風險管理模組。
*   添加參數優化功能。
*   連接實盤交易接口。