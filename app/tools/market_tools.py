# """Market data tools for fetching stock and ETF information."""

# import yfinance as yf
# import statistics


# WATCHLIST = {
#     # Index ETFs
#     "NIFTYBEES.NS": "Nifty 50 ETF",
#     "JUNIORBEES.NS": "Nifty Next 50 ETF",
#     "NIFTYNXT50.NS": "Nifty Next 50 Index Fund",
#     "MOTILALNDEX.NS": "Motilal Oswal Nifty 50 Index Fund",
    
#     # Commodity ETFs
#     "GOLDBEES.NS": "Gold ETF",
#     "SILVEBEES.NS": "Silver ETF",
    
#     # Banking & Financial ETFs
#     "BANKBEES.NS": "Nifty Bank ETF",
#     "HDFCBANK.NS": "HDFC Bank",
#     "ICICIBANK.NS": "ICICI Bank",
#     "AXISBANK.NS": "Axis Bank",
    
#     # Large Cap Stocks
#     "INFY.NS": "Infosys",
#     "TCS.NS": "Tata Consultancy Services",
#     "RELIANCE.NS": "Reliance Industries",
#     "WIPRO.NS": "Wipro",
    
#     # Pharma ETF/Stocks
#     "JUBILANTP.NS": "Jubilant Pharmova",
#     "DIVISLAB.NS": "Divi's Laboratories",
    
#     # FMCG
#     "NESTLEIND.NS": "Nestlé India",
    
#     # IT Sector ETF
#     "NIFTYIT.NS": "Nifty IT Index Fund",
    
#     # Auto Sector
#     "MARUTI.NS": "Maruti Suzuki",
    
#     # Energy
#     "POWERGRID.NS": "Power Grid Corporation",
    
#     # Healthcare
#     "APOLLOHOSP.NS": "Apollo Hospitals",
    
#     # Infrastructure
#     "BHARTIARTL.NS": "Bharti Airtel"
# }


# def fetch_market_snapshot():
#     """
#     Fetch current market data for all assets in watchlist.
#     Returns price, returns, and basic metrics.
#     """
#     data = {}

#     for ticker, name in WATCHLIST.items():
#         try:
#             stock = yf.Ticker(ticker)
#             hist = stock.history(period="1mo")

#             if not hist.empty:
#                 current = round(hist["Close"].iloc[-1], 2)
#                 start = hist["Close"].iloc[0]
#                 monthly_return = round((current - start) / start * 100, 2)
#                 daily_returns = hist["Close"].pct_change().dropna().tolist()
#                 volatility = round(statistics.stdev(daily_returns) * (252 ** 0.5) * 100, 2) if len(daily_returns) > 1 else None

#                 data[ticker] = {
#                     "name": name,
#                     "price": current,
#                     "monthly_return_pct": monthly_return,
#                     "annualized_volatility_pct": volatility,
#                     "observations": len(hist)
#                 }
#         except Exception as e:
#             data[ticker] = {
#                 "name": name,
#                 "price": None,
#                 "error": str(e)
#             }

#     return data


# def get_asset_price(ticker: str):
#     """Get current price for a specific asset."""
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period="1d")
#         if not hist.empty:
#             return round(hist["Close"].iloc[-1], 2)
#     except Exception:
#         pass
#     return None


"""Market data tools for fetching stock and ETF information."""

import contextlib
import io
import statistics

import yfinance as yf


WATCHLIST = {
    # ============================================================
    # BROAD MARKET / INDEX ETFs
    # ============================================================

    "NIFTYBEES.NS": "Nifty 50 ETF",
    "JUNIORBEES.NS": "Nifty Next 50 ETF",

    # ============================================================
    # GOLD / COMMODITIES
    # ============================================================

    "GOLDBEES.NS": "Gold ETF",
    "SILVERBEES.NS": "Silver ETF",

    # ============================================================
    # BANKING / FINANCIAL
    # ============================================================

    "BANKBEES.NS": "Nifty Bank ETF",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "AXISBANK.NS": "Axis Bank",

    # ============================================================
    # LARGE CAP / TECHNOLOGY
    # ============================================================

    "INFY.NS": "Infosys",
    "TCS.NS": "Tata Consultancy Services",
    "RELIANCE.NS": "Reliance Industries",
    "WIPRO.NS": "Wipro",

    # ============================================================
    # PHARMA / HEALTHCARE
    # ============================================================

    "DIVISLAB.NS": "Divi's Laboratories",
    "APOLLOHOSP.NS": "Apollo Hospitals",

    # ============================================================
    # FMCG
    # ============================================================

    "NESTLEIND.NS": "Nestlé India",

    # ============================================================
    # AUTOMOBILE
    # ============================================================

    "MARUTI.NS": "Maruti Suzuki",

    # ============================================================
    # ENERGY / INFRASTRUCTURE
    # ============================================================

    "POWERGRID.NS": "Power Grid Corporation",
    "BHARTIARTL.NS": "Bharti Airtel"
}


def _fetch_history_safely(ticker: str, period: str = "1mo"):
    """
    Fetch Yahoo Finance history while preventing noisy yFinance
    error messages from cluttering the application logs.

    Returns:
        DataFrame if valid data is available.
        None if Yahoo Finance returns no usable data.
    """
    try:
        stock = yf.Ticker(ticker)

        # yFinance can print warnings/errors directly to stdout/stderr
        # when Yahoo Finance has no data for a symbol.
        with contextlib.redirect_stdout(io.StringIO()):
            with contextlib.redirect_stderr(io.StringIO()):
                hist = stock.history(
                    period=period,
                    auto_adjust=False
                )

        if hist is None or hist.empty:
            return None

        return hist

    except Exception:
        return None


def fetch_market_snapshot():
    """
    Fetch current market data for all assets in the watchlist.

    Assets for which Yahoo Finance does not provide usable data
    are skipped rather than breaking the investment workflow.

    Returns:
        Dictionary containing only assets with valid market data.
    """
    data = {}

    unavailable_tickers = []

    for ticker, name in WATCHLIST.items():

        hist = _fetch_history_safely(
            ticker=ticker,
            period="1mo"
        )

        if hist is None:
            unavailable_tickers.append(ticker)
            continue

        try:
            current = round(float(hist["Close"].iloc[-1]), 2)

            start = float(hist["Close"].iloc[0])

            if start == 0:
                unavailable_tickers.append(ticker)
                continue

            monthly_return = round(
                (current - start) / start * 100,
                2
            )

            daily_returns = (
                hist["Close"]
                .pct_change()
                .dropna()
                .tolist()
            )

            volatility = None

            if len(daily_returns) > 1:
                volatility = round(
                    statistics.stdev(daily_returns)
                    * (252 ** 0.5)
                    * 100,
                    2
                )

            data[ticker] = {
                "name": name,
                "price": current,
                "monthly_return_pct": monthly_return,
                "annualized_volatility_pct": volatility,
                "observations": len(hist)
            }

        except Exception:
            unavailable_tickers.append(ticker)

    if unavailable_tickers:
        print(
            "Market data unavailable for: "
            + ", ".join(unavailable_tickers)
        )

    return data


def get_asset_price(ticker: str):
    """Get current price for a specific asset."""

    hist = _fetch_history_safely(
        ticker=ticker,
        period="1d"
    )

    if hist is None:
        return None

    try:
        return round(
            float(hist["Close"].iloc[-1]),
            2
        )
    except Exception:
        return None