from typing import Dict, Any

class CEOFusionScore:
    def __init__(self):
        # Weights
        self.weights = {
            "positioning": 0.40,
            "trend": 0.25,
            "momentum": 0.15,
            "entry_timing": 0.10,
            "risk": 0.10
        }

    def calculate(self, ta_data: Dict[str, Any], pos_data: Dict[str, Any], risk_data: Dict[str, Any]) -> float:
        """Calculate the CEO Fusion Score (0-10)."""
        
        # 1. Positioning (40%)
        pos_score = 0
        if -0.01 <= pos_data['funding_rate'] <= 0.01: pos_score += 2
        if pos_data['oi_change'] > 0: pos_score += 3
        if 0.5 <= pos_data['ls_ratio'] <= 2.0: pos_score += 3
        if not pos_data['is_crowded']: pos_score += 2
        pos_score = (pos_score / 10) * 10 # Normalize to 10
        
        # 2. Trend (25%)
        trend_score = 0
        if ta_data['market_structure'] != "SIDEWAYS": trend_score += 5
        if (ta_data['market_structure'] == "BULL" and ta_data['last_price'] > ta_data['ema_20']) or \
           (ta_data['market_structure'] == "BEAR" and ta_data['last_price'] < ta_data['ema_20']):
            trend_score += 5
        
        # 3. Momentum (15%)
        mom_score = 0
        if 40 <= ta_data['rsi'] <= 60: mom_score += 3 # Healthy RSI
        if ta_data['vol_ratio'] > 1.5: mom_score += 4
        if ta_data['dump_pump']: mom_score += 3
        mom_score = min(mom_score, 10)
        
        # 4. Entry Timing (10%)
        entry_score = 0
        if ta_data['divergence']: entry_score += 5
        # Check if near EMA 20 (within 1%)
        price_to_ema = abs(ta_data['last_price'] - ta_data['ema_20']) / ta_data['ema_20']
        if price_to_ema < 0.01: entry_score += 5
        entry_score = min(entry_score, 10)
        
        # 5. Risk (10%)
        risk_val = 0
        if risk_data['rr'] >= 2.0: risk_val += 5
        if risk_data['rr'] >= 3.0: risk_val += 5
        risk_val = min(risk_val, 10)
        
        # Final Weighted Score
        final_score = (
            pos_score * self.weights['positioning'] +
            trend_score * self.weights['trend'] +
            mom_score * self.weights['momentum'] +
            entry_score * self.weights['entry_timing'] +
            risk_val * self.weights['risk']
        )
        
        return round(final_score, 1)
