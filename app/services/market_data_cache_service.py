"""Market Data Caching Service - provides cached real-time market data."""

import yfinance as yf
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import threading
import time


class MarketDataCache:
    """In-memory cache for market data with TTL (Time To Live)."""
    
    def __init__(self, ttl_seconds: int = 300):
        """Initialize cache with TTL in seconds (default: 5 minutes)."""
        self.cache = {}
        self.timestamps = {}
        self.ttl_seconds = ttl_seconds
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        with self.lock:
            if key in self.cache:
                timestamp = self.timestamps.get(key)
                if timestamp and (datetime.now() - timestamp).total_seconds() < self.ttl_seconds:
                    return self.cache[key]
                else:
                    # Expired, remove it
                    del self.cache[key]
                    del self.timestamps[key]
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Set cache value with current timestamp."""
        with self.lock:
            self.cache[key] = value
            self.timestamps[key] = datetime.now()
    
    def clear(self) -> None:
        """Clear all cache."""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()


# Global cache instance
_market_cache = MarketDataCache(ttl_seconds=300)  # 5 minute TTL


def get_cached_price(ticker: str) -> Optional[float]:
    """Get cached price for a ticker."""
    cache_key = f"price_{ticker}"
    return _market_cache.get(cache_key)


def set_cached_price(ticker: str, price: float) -> None:
    """Set cached price for a ticker."""
    cache_key = f"price_{ticker}"
    _market_cache.set(cache_key, price)


def get_real_time_price(ticker: str) -> Dict[str, Any]:
    """
    Get real-time price for a ticker with caching.
    First checks cache, then fetches from yfinance if expired.
    """
    # Check cache first
    cached_price = get_cached_price(ticker)
    if cached_price is not None:
        return {
            "ticker": ticker,
            "price": cached_price,
            "source": "cache",
            "timestamp": datetime.now().isoformat()
        }
    
    # Fetch from yfinance
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        
        if not hist.empty:
            current_price = round(hist["Close"].iloc[-1], 2)
            set_cached_price(ticker, current_price)
            
            return {
                "ticker": ticker,
                "price": current_price,
                "source": "live",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        pass
    
    return {
        "ticker": ticker,
        "price": None,
        "error": "Could not fetch price",
        "source": "error"
    }


def get_market_data_with_cache(ticker: str, period: str = "1mo") -> Dict[str, Any]:
    """
    Get market data (OHLCV) with caching.
    Includes: price, returns, volatility, and trend.
    """
    cache_key = f"market_data_{ticker}_{period}"
    cached_data = _market_cache.get(cache_key)
    
    if cached_data is not None:
        return {**cached_data, "source": "cache"}
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return {"error": "No data available"}
        
        # Calculate metrics
        current_price = round(hist["Close"].iloc[-1], 2)
        start_price = hist["Close"].iloc[0]
        
        # Daily returns
        daily_returns = hist["Close"].pct_change().dropna().tolist()
        
        # Metrics
        period_return = round((current_price - start_price) / start_price * 100, 2)
        volatility = None
        if len(daily_returns) > 1:
            volatility = round(statistics.stdev(daily_returns) * (252 ** 0.5) * 100, 2)
        
        avg_volume = round(hist["Volume"].mean()) if "Volume" in hist else None
        high_52w = round(hist["Close"].max(), 2) if not hist.empty else None
        low_52w = round(hist["Close"].min(), 2) if not hist.empty else None
        
        data = {
            "ticker": ticker,
            "current_price": current_price,
            "period_return_pct": period_return,
            "volatility_pct": volatility,
            "avg_volume": avg_volume,
            "52w_high": high_52w,
            "52w_low": low_52w,
            "observations": len(hist),
            "daily_returns": daily_returns[-30:] if len(daily_returns) > 30 else daily_returns,  # Last 30 days
            "source": "live",
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the result
        _market_cache.set(cache_key, data)
        return data
        
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def get_all_market_data_cached(tickers: list, period: str = "1mo") -> Dict[str, Dict[str, Any]]:
    """Get market data for multiple tickers with caching."""
    results = {}
    for ticker in tickers:
        results[ticker] = get_market_data_with_cache(ticker, period)
    return results


def clear_market_cache() -> None:
    """Clear all cached market data."""
    _market_cache.clear()


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    with _market_cache.lock:
        return {
            "cached_items": len(_market_cache.cache),
            "ttl_seconds": _market_cache.ttl_seconds,
            "items": list(_market_cache.cache.keys())
        }
