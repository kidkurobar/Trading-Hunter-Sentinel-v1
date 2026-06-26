from typing import Dict, Any, Optional

class RiskManager:
    def __init__(self):
        pass

    def calculate_plan(self, side: str, entry: float, ta_data: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest SL, TP1, TP2 and calculate RR."""
        atr = ta_data.get('atr', entry * 0.01) # Fallback to 1% if ATR missing
        
        if side == "LONG":
            sl = entry - (atr * 2)
            tp1 = entry + (atr * 2)
            tp2 = entry + (atr * 4)
        else: # SHORT
            sl = entry + (atr * 2)
            tp1 = entry - (atr * 2)
            tp2 = entry - (atr * 4)
            
        risk = abs(entry - sl)
        reward = abs(tp1 - entry)
        rr = reward / risk if risk != 0 else 0
        
        return {
            "entry": entry,
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
            "rr": round(rr, 2)
        }

    def evaluate_risk(self, plan: Dict[str, Any], ta_data: Dict[str, Any]) -> Dict[str, Any]:
        """Final risk evaluation."""
        return {
            "rr": plan['rr'],
            "distance_to_sl": abs(plan['entry'] - plan['sl']) / plan['entry'] * 100,
            "volatility": ta_data.get('atr', 0) / plan['entry'] * 100
        }
