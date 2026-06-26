from typing import List, Dict, Any

class WatchlistGenerator:
    def __init__(self):
        pass

    def generate(self, all_signals: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate top 10 LONG, top 10 SHORT, and top 5 REVERSAL."""
        longs = sorted([s for s in all_signals if s['side'] == 'LONG'], key=lambda x: x['score'], reverse=True)
        shorts = sorted([s for s in all_signals if s['side'] == 'SHORT'], key=lambda x: x['score'], reverse=True)
        reversals = [s for s in all_signals if s.get('divergence')]
        
        return {
            "top_longs": longs[:10],
            "top_shorts": shorts[:10],
            "top_reversals": reversals[:5]
        }
