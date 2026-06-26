# Trading Hunter Sentinel v1

## Objective

Trading Hunter Sentinel v1 is an automated Binance Futures market scanner designed to identify high-quality trading opportunities 24/7. It leverages technical analysis, market positioning data, and a proprietary scoring mechanism (CEO Fusion Score) to filter signals, providing timely notifications via Telegram. The system also tracks the lifecycle of each alert and generates daily/weekly reports for performance analysis.

## Features

*   **24/7 Market Scanning:** Continuously monitors Binance USDT Futures market.
*   **Dynamic Scan Frequency:** Adjusts scanning frequency between 5 minutes (Normal Mode) and 1 minute (High Volatility Mode).
*   **Comprehensive Analysis:** Integrates various technical indicators (EMA, MACD, RSI, Volume, ATR, Divergence, Dump/Pump Detection) and market positioning data (Funding Rate, Open Interest, Long/Short Ratio, Crowded Trade).
*   **Hard Gate Filtering:** Applies strict criteria to reject low-quality signals before scoring.
*   **CEO Fusion Score:** Assigns a score (0-10) to each potential trade based on weighted categories (Positioning, Trend, Momentum, Entry Timing, Risk).
*   **Risk Management:** Calculates Risk/Reward (RR) and suggests Entry, Stop Loss (SL), and Take Profit (TP1, TP2) levels.
*   **Alert Lifecycle Tracking:** Monitors signals from NEW to CONFIRMED, INVALIDATED, TARGET HIT, or STOPPED.
*   **Duplicate Signal Filter:** Prevents redundant notifications.
*   **Telegram Notifications:** Sends real-time trade alerts, lifecycle updates, and watchlist summaries.
*   **Watchlist Generation:** Creates Top 10 LONG, Top 10 SHORT, and Top 5 REVERSAL lists every 30 minutes.
*   **Daily & Weekly Reports:** Provides performance summaries and market insights.

## System Architecture

For a detailed overview of the system's design, please refer to the `system_architecture.md` file.

## Setup and Deployment

This system is designed to run continuously in a **persistent environment**. The recommended deployment option is **Manus WebDev Reserved Hosting** due to its ability to maintain a single, always-on process, which is ideal for 24/7 scanning and high-frequency operations. Alternatively, a Cloud Computer (Persistent Sandbox) can be used if more advanced customization or resources are required.

### 1. Prerequisites

*   **Python 3.9+**
*   **pip** (Python package installer)
*   **Telegram Bot Token and Chat ID:** You have provided these, and they are hardcoded in `main.py` for simplicity. For production, it's recommended to use environment variables.
    *   `TELEGRAM_TOKEN`: `8837408072:AAE4TDTrLnXHI4G79QcNMpU0Cj_O7IT4zRo`
    *   `CHAT_ID`: `6652792902`

### 2. Installation

1.  **Clone the repository (or create the files manually):**
    ```bash
    # If you have git access
    git clone <repository_url>
    cd trading_hunter_sentinel
    
    # If creating manually, ensure all files are in the correct directory structure
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd trading_hunter_sentinel
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

*   **Telegram Credentials:** The `TELEGRAM_TOKEN` and `CHAT_ID` are currently hardcoded in `main.py`. If you wish to change them or move them to environment variables, edit `main.py` accordingly.
*   **Scanning Parameters:** Adjust `min_rr` and `min_vol_ratio` in `signal_generation/hard_gate.py` if needed. The CEO Fusion Score weights are in `signal_generation/ceo_fusion_score.py`.
*   **Market Universe:** The system currently scans up to 200 USDT Futures symbols. This can be adjusted in `main.py` within the `refresh_symbols` method.

### 4. Running the Scanner

To start the Trading Hunter Sentinel, execute the `main.py` script:

```bash
python3 main.py
```

This will start the scanner, refresh symbols, perform an initial scan, and then schedule subsequent scans and watchlist generations according to the defined frequencies. The script will run indefinitely until manually stopped.

### 5. Stopping the Scanner

To stop the scanner, you can typically use `Ctrl+C` in the terminal where it's running. In a persistent hosting environment, you would use the platform's controls to stop the running process.

## Project Structure

```
trading_hunter_sentinel/
├── main.py                     # Main application entry point, scheduler setup
├── config.py                   # Configuration settings (API keys, Telegram details, thresholds) - *Currently integrated into main.py for simplicity*
├── data_ingestion/             # Module for fetching data from Binance
│   ├── binance_client.py
│   └── __init__.py
├── analysis/                   # Module for technical analysis and market data processing
│   ├── ta_engine.py
│   ├── positioning_processor.py
│   └── __init__.py
├── signal_generation/          # Module for signal filtering, scoring, and management
│   ├── hard_gate.py
│   ├── ceo_fusion_score.py
│   ├── risk_manager.py
│   ├── alert_lifecycle.py
│   ├── duplicate_filter.py
│   └── __init__.py
├── notifications/              # Module for Telegram interactions and report generation
│   ├── telegram_bot.py
│   ├── watchlist_generator.py
│   ├── report_generator.py     # *Placeholder for future daily/weekly report logic*
│   └── __init__.py
├── utils/                      # Utility functions (logging, data structures, etc.) - *Placeholder*
│   ├── logger.py               # *Placeholder*
│   └── __init__.py
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Future Enhancements (Roadmap)

As per your initial request, the system is designed with future enhancements in mind:

*   **Version 2: Watchlist Engine:** Already integrated.
*   **Version 3: Position Assistant:** Requires user input for open positions and real-time re-evaluation.
*   **Version 4: Trade Journal:** Integration with a journaling system to track trades and performance.
*   **Version 5: Performance Analytics:** Advanced analytics based on trade journal data.
*   **Version 6: AI Risk Manager:** More sophisticated risk assessment using AI.
*   **Version 7: Semi-Auto Trading:** Partial automation of trade execution.
*   **Version 8: Fully Automated Trading:** Full automation of trade execution.

## Important Notes

*   **Error Handling:** Basic error handling is implemented, but robust logging and more sophisticated error recovery mechanisms would be beneficial for a production system.
*   **High Volatility Mode:** The logic for switching to High Volatility Mode (1-minute scan frequency) is not yet implemented. This would require a mechanism to detect market volatility and dynamically adjust the `schedule`.
*   **Daily/Weekly Reports:** The `report_generator.py` is a placeholder. The actual logic for generating comprehensive daily and weekly reports needs to be implemented.
*   **Liquidation & Spread:** The current implementation does not explicitly fetch liquidation data or calculate spread. These can be integrated by extending the `BinanceFuturesClient` and `HardGate` classes.

---

**Author:** Manus AI
**Date:** June 26, 2026
