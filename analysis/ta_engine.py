import pandas as pd
import pandas_ta as ta
import numpy as np
from typing import Dict, Any, Optional

class TAEngine:
    def __init__(self):
        pass

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all required technical indicators."""
        # EMA
        df['ema_9'] = ta.ema(df['close'], length=9)
        df['ema_20'] = ta.ema(df['close'], length=20)
        df['ema_50'] = ta.ema(df['close'], length=50)
        df['ema_200'] = ta.ema(df['close'], length=200)
        
        # MACD
        macd = ta.macd(df['close'])
        df = pd.concat([df, macd], axis=1)
        
        # RSI
        df['rsi'] = ta.rsi(df['close'], length=14)
        
        # Volume
        df['vol_ma_20'] = ta.sma(df['volume'], length=20)
        df['vol_ratio'] = df['volume'] / df['vol_ma_20']
        
        # ATR
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        # Bollinger Bands
        bbands = ta.bbands(df['close'], length=20, std=2)
        df = pd.concat([df, bbands], axis=1)
        
        return df

    def detect_market_structure(self, df: pd.DataFrame) -> str:
        """Detect current market structure (BULL, BEAR, SIDEWAYS)."""
        last_close = df['close'].iloc[-1]
        ema_20 = df['ema_20'].iloc[-1]
        ema_50 = df['ema_50'].iloc[-1]
        ema_200 = df['ema_200'].iloc[-1]
        
        if last_close > ema_50 > ema_200:
            return "BULL"
        elif last_close < ema_50 < ema_200:
            return "BEAR"
        else:
            return "SIDEWAYS"

    def detect_dump_pump(self, df: pd.DataFrame, window: int = 5, threshold: float = 2.0) -> Optional[str]:
        """Detect sudden price pumps or dumps."""
        recent_change = (df['close'].iloc[-1] - df['close'].iloc[-window]) / df['close'].iloc[-window] * 100
        if recent_change >= threshold:
            return "PUMP"
        elif recent_change <= -threshold:
            return "DUMP"
        return None

    def detect_divergence(self, df: pd.DataFrame, window: int = 20) -> Optional[str]:
        """Detect RSI divergence (Bullish or Bearish)."""
        # Simplified divergence detection
        price = df['close'].iloc[-window:]
        rsi = df['rsi'].iloc[-window:]
        
        # Bullish Divergence: Price lower low, RSI higher low
        if price.iloc[-1] < price.min() and rsi.iloc[-1] > rsi.min():
            return "BULLISH_DIVERGENCE"
        
        # Bearish Divergence: Price higher high, RSI lower high
        if price.iloc[-1] > price.max() and rsi.iloc[-1] < rsi.max():
            return "BEARISH_DIVERGENCE"
            
        return None

    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive technical analysis summary."""
        df = self.calculate_indicators(df)
        last_row = df.iloc[-1]
        
        return {
            "last_price": last_row['close'],
            "ema_9": last_row['ema_9'],
            "ema_20": last_row['ema_20'],
            "ema_50": last_row['ema_50'],
            "ema_200": last_row['ema_200'],
            "rsi": last_row['rsi'],
            "vol_ratio": last_row['vol_ratio'],
            "market_structure": self.detect_market_structure(df),
            "dump_pump": self.detect_dump_pump(df),
            "divergence": self.detect_divergence(df)
        }
