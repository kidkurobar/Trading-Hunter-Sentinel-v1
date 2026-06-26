import requests
import pandas as pd
import time
from typing import List, Dict, Optional

class BinanceFuturesClient:
    BASE_URL = "https://fapi.binance.com"
    
    def __init__(self):
        pass

    def get_exchange_info(self) -> List[str]:
        """Fetch all active USDT futures symbols."""
        url = f"{self.BASE_URL}/fapi/v1/exchangeInfo"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        symbols = [
            s['symbol'] for s in data['symbols'] 
            if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING'
        ]
        return symbols

    def get_klines(self, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV data for a symbol."""
        url = f"{self.BASE_URL}/fapi/v1/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
            
        return df

    def get_funding_rate(self, symbol: str) -> Optional[float]:
        """Fetch current funding rate for a symbol."""
        url = f"{self.BASE_URL}/fapi/v1/premiumIndex"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data.get('lastFundingRate', 0))

    def get_open_interest(self, symbol: str) -> Optional[float]:
        """Fetch current open interest for a symbol."""
        url = f"{self.BASE_URL}/fapi/v1/openInterest"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data.get('openInterest', 0))

    def get_open_interest_statistics(self, symbol: str, period: str = '5m', limit: int = 10) -> List[Dict]:
        """Fetch historical open interest statistics."""
        url = f"{self.BASE_URL}/futures/data/openInterestHist"
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_long_short_ratio(self, symbol: str, period: str = '5m', limit: int = 10) -> List[Dict]:
        """Fetch global long/short ratio statistics."""
        url = f"{self.BASE_URL}/futures/data/globalLongShortAccountRatio"
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_24h_ticker(self, symbol: Optional[str] = None) -> List[Dict]:
        """Fetch 24h ticker price change statistics."""
        url = f"{self.BASE_URL}/fapi/v1/ticker/24hr"
        params = {"symbol": symbol} if symbol else {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else [data]
