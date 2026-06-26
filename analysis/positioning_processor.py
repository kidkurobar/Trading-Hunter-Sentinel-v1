from typing import Dict, List, Any, Optional
import pandas as pd

class PositioningProcessor:
    def __init__(self):
        pass

    def process_oi_change(self, oi_hist: List[Dict]) -> float:
        """Calculate percentage change in Open Interest."""
        if len(oi_hist) < 2:
            return 0.0
        latest_oi = float(oi_hist[-1]['sumOpenInterest'])
        previous_oi = float(oi_hist[0]['sumOpenInterest'])
        if previous_oi == 0:
            return 0.0
        return (latest_oi - previous_oi) / previous_oi * 100

    def process_long_short_ratio(self, ls_hist: List[Dict]) -> float:
        """Get the latest long/short account ratio."""
        if not ls_hist:
            return 1.0
        return float(ls_hist[-1]['longShortRatio'])

    def detect_crowded_trade(self, funding_rate: float, ls_ratio: float) -> bool:
        """Detect if a trade is 'crowded' (excessive bias)."""
        # Thresholds can be adjusted
        if abs(funding_rate) > 0.05 or ls_ratio > 3.0 or ls_ratio < 0.33:
            return True
        return False

    def analyze(self, funding_rate: float, oi_hist: List[Dict], ls_hist: List[Dict]) -> Dict[str, Any]:
        """Summary of positioning data."""
        oi_change = self.process_oi_change(oi_hist)
        ls_ratio = self.process_long_short_ratio(ls_hist)
        
        return {
            "funding_rate": funding_rate,
            "oi_change": oi_change,
            "ls_ratio": ls_ratio,
            "is_crowded": self.detect_crowded_trade(funding_rate, ls_ratio)
        }
