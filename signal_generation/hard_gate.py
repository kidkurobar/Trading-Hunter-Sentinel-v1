from typing import Dict, Any, Tuple

class HardGate:
    def __init__(self, min_rr: float = 1.8, min_vol_ratio: float = 0.5):
        self.min_rr = min_rr
        self.min_vol_ratio = min_vol_ratio

    def check(self, ta_data: Dict[str, Any], pos_data: Dict[str, Any], rr: float) -> Tuple[bool, str]:
        """Check if signal passes the Hard Gate criteria."""
        
        # 1. Funding Available (Implicitly checked by fetching, but can check for extreme values)
        if pos_data['funding_rate'] is None:
            return False, "Funding Missing"
        
        # 2. RR < 1.8 -> Reject
        if rr < self.min_rr:
            return False, f"Low RR: {rr:.2f}"
        
        # 3. Volume below threshold -> Reject
        if ta_data['vol_ratio'] < self.min_vol_ratio:
            return False, f"Low Volume Ratio: {ta_data['vol_ratio']:.2f}"
        
        # 4. OI confirmation -> Reject if OI is declining significantly
        if pos_data['oi_change'] < -5.0:
            return False, f"OI Declining: {pos_data['oi_change']:.2f}%"
        
        # 5. Crowded Trade -> Reject
        if pos_data['is_crowded']:
            return False, "Crowded Trade"
            
        # 6. Spread (Simplified check: can be added if order book data is fetched)
        
        return True, "Passed"
