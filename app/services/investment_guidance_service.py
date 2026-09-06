"""Investment guidance service - provides detailed steps and resources for each investment."""

from typing import Dict, List, Any


# Detailed investment guidance with steps and resources
INVESTMENT_GUIDANCE_DB = {
    # Index ETFs
    "NIFTYBEES.NS": {
        "name": "Nifty 50 ETF (BeES)",
        "category": "Index ETF",
        "description": "Exchange Traded Fund tracking Nifty 50 index - top 50 large-cap Indian companies",
        "risk_level": "Medium",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open a Demat Account",
                "description": "You need a Demat (Dematerialized) account to hold ETF shares digitally.",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                    {"name": "Upstox", "url": "https://upstox.com/signup"},
                    {"name": "Shoonya (CHOSL)", "url": "https://shoonya.com/"}
                ],
                "timeline": "2-3 working days",
                "charges": "Mostly free or ₹0-500 opening charges"
            },
            {
                "step": 2,
                "title": "Open a Trading Account",
                "description": "Once Demat is ready, you need a Trading account with a broker to buy/sell ETFs.",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                    {"name": "Upstox", "url": "https://upstox.com/signup"},
                ],
                "timeline": "Instant (with Demat)",
                "charges": "Free with most brokers"
            },
            {
                "step": 3,
                "title": "Fund Your Trading Account",
                "description": "Add money to your trading account via bank transfer, UPI, or NetBanking.",
                "timeline": "Instant to 2 hours",
                "charges": "No charges on most platforms"
            },
            {
                "step": 4,
                "title": "Place an Order",
                "description": "Log into your trading platform, search for NIFTYBEES.NS, and place a buy order for your desired quantity.",
                "instructions": [
                    "Open broker app/website",
                    "Go to 'Buy' section",
                    "Search for NIFTYBEES.NS",
                    "Select quantity (1 unit = 1 share)",
                    "Choose order type (Market/Limit)",
                    "Review and confirm"
                ],
                "average_cost": "~₹100-200 per unit (Check current price)"
            },
            {
                "step": 5,
                "title": "Hold and Monitor",
                "description": "Your ETF units will be held in your Demat account. Monitor performance regularly.",
                "timeline": "Long-term (5+ years for better returns)"
            }
        ],
        "best_for": "Long-term wealth creation, diversified equity exposure",
        "yearly_return": "~12-15% (historical average)",
        "expense_ratio": "0.04%",
        "liquidity": "Highly liquid, can sell anytime during market hours",
        "taxes": "Long-term capital gains tax: 12.5% (hold > 12 months); Short-term: 15%"
    },
    
    "JUNIORBEES.NS": {
        "name": "Nifty Next 50 ETF (JuniorBees)",
        "category": "Index ETF",
        "description": "Exchange Traded Fund tracking Nifty Next 50 - mid-cap companies with growth potential",
        "risk_level": "Medium-High",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open a Demat Account",
                "description": "Required to hold ETF shares digitally.",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                    {"name": "Upstox", "url": "https://upstox.com/signup"},
                ],
                "timeline": "2-3 working days"
            },
            {
                "step": 2,
                "title": "Fund Your Account",
                "description": "Transfer money to your trading account"
            },
            {
                "step": 3,
                "title": "Buy JUNIORBEES.NS",
                "description": "Place buy order through your trading platform"
            }
        ],
        "best_for": "Growth-seeking investors, medium-term horizon",
        "yearly_return": "~15-18% (historical average)",
        "expense_ratio": "0.04%",
        "liquidity": "Highly liquid",
        "taxes": "Capital gains tax based on holding period"
    },
    
    "GOLDBEES.NS": {
        "name": "Gold ETF (GoldBees)",
        "category": "Commodity ETF",
        "description": "Exchange Traded Fund tracking gold prices - hedge against inflation",
        "risk_level": "Low-Medium",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open a Demat Account",
                "description": "Digital account needed for holding Gold ETF.",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                    {"name": "Upstox", "url": "https://upstox.com/signup"},
                ]
            },
            {
                "step": 2,
                "title": "Place Order",
                "description": "Buy Gold ETF shares - acts as digital gold"
            }
        ],
        "best_for": "Portfolio diversification, inflation hedge",
        "yearly_return": "~2-5% (variable with gold prices)",
        "expense_ratio": "0.01-0.02%",
        "liquidity": "Very liquid, can sell instantly",
        "advantages": "No storage cost, No purity concerns, Tax-efficient"
    },
    
    "HDFCBANK.NS": {
        "name": "HDFC Bank Limited",
        "category": "Large Cap Stock",
        "description": "India's leading private sector bank with strong fundamentals",
        "risk_level": "Medium",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open Demat & Trading Account",
                "description": "Necessary to buy individual stocks.",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                ],
                "timeline": "2-3 working days"
            },
            {
                "step": 2,
                "title": "Research the Stock",
                "description": "Check latest financial reports, P/E ratio, dividend history",
                "resources": [
                    {"name": "BSE India", "url": "https://www.bseindia.com"},
                    {"name": "NSE India", "url": "https://www.nseindia.com"},
                    {"name": "Moneycontrol", "url": "https://www.moneycontrol.com"}
                ]
            },
            {
                "step": 3,
                "title": "Place a Buy Order",
                "description": "Search HDFCBANK.NS and place order with desired quantity"
            }
        ],
        "best_for": "Long-term investors, dividend seekers",
        "yearly_return": "~12-15% (historical)",
        "dividend_yield": "~2-3%",
        "pe_ratio": "Variable (check current)",
        "market_cap": "₹18+ lakh crore"
    },
    
    "INFY.NS": {
        "name": "Infosys Limited",
        "category": "Large Cap Stock (IT)",
        "description": "India's second-largest IT consulting company",
        "risk_level": "Medium",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open Trading & Demat Account",
                "description": "Open Demat and Trading account with any authorized broker",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                ]
            },
            {
                "step": 2,
                "title": "Fund Your Account",
                "description": "Add required capital via bank transfer or UPI"
            },
            {
                "step": 3,
                "title": "Buy INFY.NS",
                "description": "Place market or limit order through your broker platform"
            }
        ],
        "best_for": "Dividend seekers, stable growth investors",
        "yearly_return": "~10-14% (historical)",
        "dividend_yield": "~1.5-2%"
    },
    
    "BANKBEES.NS": {
        "name": "Nifty Bank ETF (BankBees)",
        "category": "Sector ETF",
        "description": "ETF tracking top 12 banking companies in India",
        "risk_level": "Medium",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open Demat Account",
                "description": "Open a Demat account with any authorized broker for digital holding of ETF shares",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                ]
            },
            {
                "step": 2,
                "title": "Buy BANKBEES.NS",
                "description": "Place a buy order to get instant banking sector exposure"
            }
        ],
        "best_for": "Banking sector investors, diversified bank exposure",
        "yearly_return": "~12-16%",
        "expense_ratio": "0.07%"
    },
    
    "TCS.NS": {
        "name": "Tata Consultancy Services",
        "category": "Large Cap Stock (IT)",
        "description": "India's largest IT company and most valuable software services company",
        "risk_level": "Medium-Low",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open Demat & Trading Account",
                "description": "Open Demat and Trading accounts to buy individual stock shares",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                ]
            },
            {
                "step": 2,
                "title": "Place Order for TCS.NS",
                "description": "Buy shares through your broker with desired quantity"
            }
        ],
        "best_for": "Dividend investors, blue-chip stock portfolio",
        "yearly_return": "~8-12%",
        "dividend_yield": "~1.2-1.8%"
    },
    
    "RELIANCE.NS": {
        "name": "Reliance Industries Limited",
        "category": "Large Cap Stock",
        "description": "India's most valuable company, diversified across oil, chemicals, retail, telecom",
        "risk_level": "Medium",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open Demat Account",
                "description": "Open a Demat account with any authorized broker to hold Reliance shares digitally",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                ]
            },
            {
                "step": 2,
                "title": "Buy RELIANCE.NS",
                "description": "Place a buy order to invest in India's most valuable company"
            }
        ],
        "best_for": "Long-term wealth creation, defensive portfolio",
        "yearly_return": "~10-15%",
        "market_cap": "₹19+ lakh crore"
    }
}


def get_investment_guidance(symbol: str) -> Dict[str, Any]:
    """Get detailed investment guidance for a symbol."""
    return INVESTMENT_GUIDANCE_DB.get(symbol, {
        "name": symbol,
        "category": "Investment",
        "description": f"Detailed guidance for {symbol}",
        "investment_steps": [
            {
                "step": 1,
                "title": "Open Demat Account",
                "description": "Open a Demat account with any authorized broker",
                "platforms": [
                    {"name": "Zerodha", "url": "https://zerodha.com/open-account"},
                    {"name": "Angel One", "url": "https://www.angelone.in/open-account"},
                    {"name": "Upstox", "url": "https://upstox.com/signup"},
                ]
            },
            {
                "step": 2,
                "title": "Fund Your Account",
                "description": "Transfer money to your trading account"
            },
            {
                "step": 3,
                "title": "Place Buy Order",
                "description": f"Search for {symbol} and place a buy order"
            }
        ]
    })


def get_investment_steps_summary(symbol: str) -> str:
    """Get a text summary of investment steps."""
    guidance = get_investment_guidance(symbol)
    steps_text = f"\n\n📈 How to invest in {guidance.get('name', symbol)}:\n"
    steps_text += f"Category: {guidance.get('category', 'Investment')}\n"
    steps_text += f"Risk Level: {guidance.get('risk_level', 'Medium')}\n\n"
    
    for step in guidance.get('investment_steps', []):
        steps_text += f"**Step {step.get('step', '?')}: {step.get('title', 'Investment Step')}**\n"
        steps_text += f"{step.get('description', '')}\n"
        
        if step.get('platforms'):
            steps_text += "Popular platforms: "
            platforms = [f"[{p['name']}]({p['url']})" for p in step['platforms']]
            steps_text += ", ".join(platforms) + "\n"
        
        steps_text += "\n"
    
    return steps_text
