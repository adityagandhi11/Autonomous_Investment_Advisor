"""Market data tools for fetching stock and ETF information."""

import yfinance as yf
import statistics


WATCHLIST = {
    # Index ETFs
    "NIFTYBEES.NS": "Nifty 50 ETF",
    "JUNIORBEES.NS": "Nifty Next 50 ETF",
    "NIFTYNXT50.NS": "Nifty Next 50 Index Fund",
    "MOTILALNDEX.NS": "Motilal Oswal Nifty 50 Index Fund",
    
    # Commodity ETFs
    "GOLDBEES.NS": "Gold ETF",
    "SILVEBEES.NS": "Silver ETF",
    
    # Banking & Financial ETFs
    "BANKBEES.NS": "Nifty Bank ETF",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "AXISBANK.NS": "Axis Bank",
    
    # Large Cap Stocks
    "INFY.NS": "Infosys",
    "TCS.NS": "Tata Consultancy Services",
    "RELIANCE.NS": "Reliance Industries",
    "WIPRO.NS": "Wipro",
    
    # Pharma ETF/Stocks
    "JUBILANTP.NS": "Jubilant Pharmova",
    "DIVISLAB.NS": "Divi's Laboratories",
    
    # FMCG
    "NESTLEIND.NS": "Nestlé India",
    
    # IT Sector ETF
    "NIFTYIT.NS": "Nifty IT Index Fund",
    
    # Auto Sector
    "MARUTI.NS": "Maruti Suzuki",
    
    # Energy
    "POWERGRID.NS": "Power Grid Corporation",
    
    # Healthcare
    "APOLLOHOSP.NS": "Apollo Hospitals",
    
    # Infrastructure
    "BHARTIARTL.NS": "Bharti Airtel"
}


def fetch_market_snapshot():
    """
    Fetch current market data for all assets in watchlist.
    Returns price, returns, and basic metrics.
    """
    data = {}

    for ticker, name in WATCHLIST.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")

            if not hist.empty:
                current = round(hist["Close"].iloc[-1], 2)
                start = hist["Close"].iloc[0]
                monthly_return = round((current - start) / start * 100, 2)
                daily_returns = hist["Close"].pct_change().dropna().tolist()
                volatility = round(statistics.stdev(daily_returns) * (252 ** 0.5) * 100, 2) if len(daily_returns) > 1 else None

                data[ticker] = {
                    "name": name,
                    "price": current,
                    "monthly_return_pct": monthly_return,
                    "annualized_volatility_pct": volatility,
                    "observations": len(hist)
                }
        except Exception as e:
            data[ticker] = {
                "name": name,
                "price": None,
                "error": str(e)
            }

    return data


def get_asset_price(ticker: str):
    """Get current price for a specific asset."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            return round(hist["Close"].iloc[-1], 2)
    except Exception:
        pass
    return None
