import requests
from typing import Dict, Any, List

class TelegramBot:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_message(self, text: str):
        url = f"{self.base_url}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

    def format_signal(self, signal: Dict[str, Any]) -> str:
        side_emoji = "🚀" if signal['side'] == "LONG" else "🔻"
        text = (
            f"🚨 *HIGH CONFIDENCE SIGNAL*\n\n"
            f"{side_emoji} *{signal['side']}*\n"
            f"*{signal['symbol']}*\n\n"
            f"Price: `{signal['price']}`\n"
            f"Timeframe: `{signal['timeframe']}`\n"
            f"CEO Score: `{signal['score']} / 10`\n\n"
            f"Funding: `{signal['pos_data']['funding_rate']:.4f}%`\n"
            f"OI: `{signal['pos_data']['oi_change']:.1f}%`\n"
            f"Volume: `{signal['ta_data']['vol_ratio']:.1f}x`\n\n"
            f"*Reason*\n"
            f"• {signal['ta_data']['market_structure']} Trend\n"
            f"• RSI: {signal['ta_data']['rsi']:.1f}\n"
            f"{'• Divergence Detected' if signal['ta_data']['divergence'] else ''}\n\n"
            f"*Suggested Plan*\n"
            f"Entry: `{signal['plan']['entry']}`\n"
            f"SL: `{signal['plan']['sl']:.2f}`\n"
            f"TP1: `{signal['plan']['tp1']:.2f}`\n"
            f"TP2: `{signal['plan']['tp2']:.2f}`\n"
            f"RR: `1 : {signal['plan']['rr']}`"
        )
        return text

    def format_lifecycle_update(self, symbol: str, status: str, price: float) -> str:
        emoji = "✅" if status == "TARGET HIT" else "❌"
        return f"{emoji} *ALERT UPDATE: {symbol}*\nStatus: `{status}`\nCurrent Price: `{price}`"

    def format_watchlist(self, watchlist: Dict[str, List[Dict[str, Any]]]) -> str:
        text = "📋 *WATCHLIST UPDATE*\n\n"
        text += "*Top 10 LONG*\n"
        for s in watchlist['top_longs']:
            text += f"- {s['symbol']} (Score: {s['score']})\n"
        text += "\n*Top 10 SHORT*\n"
        for s in watchlist['top_shorts']:
            text += f"- {s['symbol']} (Score: {s['score']})\n"
        return text
