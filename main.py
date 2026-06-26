import time
import schedule
from data_ingestion.binance_client import BinanceFuturesClient
from analysis.ta_engine import TAEngine
from analysis.positioning_processor import PositioningProcessor
from signal_generation.hard_gate import HardGate
from signal_generation.ceo_fusion_score import CEOFusionScore
from signal_generation.risk_manager import RiskManager
from signal_generation.alert_lifecycle import AlertLifecycle
from notifications.telegram_bot import TelegramBot
from notifications.watchlist_generator import WatchlistGenerator

# Configuration
TELEGRAM_TOKEN = "8837408072:AAE4TDTrLnXHI4G79QcNMpU0Cj_O7IT4zRo"
CHAT_ID = "6652792902"

class TradingSentinel:
    def __init__(self):
        self.binance = BinanceFuturesClient()
        self.ta_engine = TAEngine()
        self.pos_processor = PositioningProcessor()
        self.hard_gate = HardGate()
        self.ceo_scorer = CEOFusionScore()
        self.risk_manager = RiskManager()
        self.lifecycle = AlertLifecycle()
        self.telegram = TelegramBot(TELEGRAM_TOKEN, CHAT_ID)
        self.watchlist_gen = WatchlistGenerator()
        
        self.symbols = []
        self.all_signals = []

    def refresh_symbols(self):
        """Update the list of symbols to scan."""
        try:
            all_symbols = self.binance.get_exchange_info()
            # Sort by volume or just take top 200
            self.symbols = all_symbols[:200]
            print(f"Refreshed {len(self.symbols)} symbols.")
        except Exception as e:
            print(f"Error refreshing symbols: {e}")

    def scan(self):
        """Main scan logic."""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting scan...")
        self.all_signals = []
        
        for symbol in self.symbols:
            try:
                # 1. Fetch Data
                df = self.binance.get_klines(symbol, interval='1h', limit=100)
                if df.empty or len(df) < 50: continue
                
                funding = self.binance.get_funding_rate(symbol)
                oi_hist = self.binance.get_open_interest_statistics(symbol, period='5m', limit=10)
                ls_hist = self.binance.get_long_short_ratio(symbol, period='5m', limit=10)
                
                # 2. Analyze
                ta_data = self.ta_engine.analyze(df)
                pos_data = self.pos_processor.analyze(funding, oi_hist, ls_hist)
                
                # 3. Determine Side
                side = "LONG" if ta_data['market_structure'] == "BULL" else "SHORT"
                
                # 4. Risk Plan
                plan = self.risk_manager.calculate_plan(side, ta_data['last_price'], ta_data)
                risk_eval = self.risk_manager.evaluate_risk(plan, ta_data)
                
                # 5. Hard Gate
                passed, reason = self.hard_gate.check(ta_data, pos_data, plan['rr'])
                
                # 6. Scoring
                score = self.ceo_scorer.calculate(ta_data, pos_data, risk_eval)
                
                signal = {
                    "symbol": symbol,
                    "side": side,
                    "price": ta_data['last_price'],
                    "timeframe": "1H",
                    "score": score,
                    "ta_data": ta_data,
                    "pos_data": pos_data,
                    "plan": plan,
                    "passed_gate": passed,
                    "gate_reason": reason
                }
                
                if passed:
                    self.all_signals.append(signal)
                    
                    # 7. Alert Logic
                    if score >= 7.0 and self.lifecycle.should_send_new(symbol, side, ta_data['last_price'], "1H"):
                        self.telegram.send_message(self.telegram.format_signal(signal))
                        self.lifecycle.update_alert(symbol, side, ta_data['last_price'], "1H", score)
                        self.lifecycle.active_alerts[symbol]['plan'] = plan
                
                # 8. Lifecycle Tracking
                lifecycle_status = self.lifecycle.check_lifecycle(symbol, ta_data['last_price'])
                if lifecycle_status:
                    self.telegram.send_message(self.telegram.format_lifecycle_update(symbol, lifecycle_status, ta_data['last_price']))

            except Exception as e:
                # print(f"Error scanning {symbol}: {e}")
                continue
        
        print(f"Scan complete. Found {len(self.all_signals)} valid signals passing Hard Gate.")

    def run_watchlist(self):
        """Generate and send watchlist."""
        print("Generating watchlist...")
        if self.all_signals:
            watchlist = self.watchlist_gen.generate(self.all_signals)
            self.telegram.send_message(self.telegram.format_watchlist(watchlist))

def main():
    sentinel = TradingSentinel()
    sentinel.refresh_symbols()
    
    # Initial scan
    sentinel.scan()
    sentinel.run_watchlist()
    
    # Schedule
    schedule.every(5).minutes.do(sentinel.scan)
    schedule.every(30).minutes.do(sentinel.run_watchlist)
    schedule.every(24).hours.do(sentinel.refresh_symbols)
    
    print("Sentinel is running...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
