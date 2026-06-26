import time
from typing import Dict, List, Optional

class AlertLifecycle:
    def __init__(self, expiry_minutes: int = 60):
        self.active_alerts = {} # symbol -> alert_data
        self.expiry_seconds = expiry_minutes * 60

    def should_send_new(self, symbol: str, side: str, price: float, timeframe: str) -> bool:
        """Check if a new alert should be sent based on duplicate filters."""
        if symbol not in self.active_alerts:
            return True
            
        last_alert = self.active_alerts[symbol]
        
        # 1. Complete 60 minutes?
        if time.time() - last_alert['timestamp'] > self.expiry_seconds:
            return True
            
        # 2. Side changed?
        if last_alert['side'] != side:
            return True
            
        # 3. Timeframe changed?
        if last_alert['timeframe'] != timeframe:
            return True
            
        # 4. Price changed > 2%?
        price_change = abs(price - last_alert['price']) / last_alert['price'] * 100
        if price_change > 2.0:
            return True
            
        return False

    def update_alert(self, symbol: str, side: str, price: float, timeframe: str, score: float):
        """Register or update an alert in the system."""
        self.active_alerts[symbol] = {
            "symbol": symbol,
            "side": side,
            "price": price,
            "timeframe": timeframe,
            "score": score,
            "timestamp": time.time(),
            "status": "NEW"
        }

    def check_lifecycle(self, symbol: str, current_price: float) -> Optional[str]:
        """Track alert status (NEW -> CONFIRMED -> TARGET HIT -> STOPPED)."""
        if symbol not in self.active_alerts:
            return None
            
        alert = self.active_alerts[symbol]
        plan = alert.get('plan')
        if not plan: return None
        
        status_update = None
        
        if alert['side'] == "LONG":
            if current_price >= plan['tp1'] and alert['status'] != "TARGET HIT":
                status_update = "TARGET HIT"
            elif current_price <= plan['sl'] and alert['status'] != "STOPPED":
                status_update = "STOPPED"
        else: # SHORT
            if current_price <= plan['tp1'] and alert['status'] != "TARGET HIT":
                status_update = "TARGET HIT"
            elif current_price >= plan['sl'] and alert['status'] != "STOPPED":
                status_update = "STOPPED"
                
        if status_update:
            alert['status'] = status_update
            return status_update
            
        return None
