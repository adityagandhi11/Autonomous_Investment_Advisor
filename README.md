# Autonomous Investment Research & Portfolio Advisor

**Production-grade Agentic AI using Python, LangChain, LangGraph, FastAPI, and MongoDB**

---

## Overview

An autonomous AI-powered investment advisor that creates personalized, diversified portfolios by:

1. **Understanding** investment goals and constraints
2. **Profiling** investor risk tolerance
3. **Researching** real-time market data
4. **Building** diversified asset allocation
5. **Critiquing** its own recommendations with a reflection loop
6. **Storing** portfolio history for future rebalancing

### Example Query

> "I want to invest ₹50,000 for 5 years with moderate risk."

**System Response:**
- ✅ Risk Profile: Moderate
- 📊 Portfolio: 45% Nifty ETF, 20% Nifty Next 50, 20% Gold ETF, 15% HDFC Bank
- 📝 Critique: "Portfolio approved - meets diversification requirements"
- 🔄 Workflow History: Full decision trace from all agents

---

## Architecture

```
FastAPI Endpoint
    ↓
LangGraph Workflow
    ↓
┌─────────────────────┐
│ Planner Agent       │ → Breaks goal into steps
├─────────────────────┤
│ Risk Profiler       │ → Determines risk category
├─────────────────────┤
│ Market Research     │ → Fetches real-time data
├─────────────────────┤
│ Portfolio Builder   │ → Allocates assets
├─────────────────────┤
│ Critic Agent        │ → Validates & critiques
└─────────────────────┘
    ↓ (conditional)
[Approved] → MongoDB + Return Response
[Revise]   → Portfolio Builder (reflection loop)
```

---

## Project Structure

```
investment-advisor-agent/
├── app/
│   ├── main.py                  # FastAPI application
│   ├── graph.py                 # LangGraph workflow
│   ├── state.py                 # Shared state TypedDict
│   ├── config.py                # Configuration management
│   │
│   ├── agents/
│   │   ├── planner.py           # Planning agent
│   │   ├── risk_profiler.py     # Risk assessment agent
│   │   ├── market_research.py   # Market data agent
│   │   ├── portfolio_builder.py # Portfolio construction agent
│   │   ├── critic.py            # Validation & critique agent
│   │   └── rebalancer.py        # Portfolio rebalancing agent
│   │
│   ├── tools/
│   │   ├── market_tools.py      # yFinance integration
│   │   ├── news_fetcher.py      # News API integration
│   │   └── calculators.py       # Financial calculations
│   │
│   ├── services/
│   │   ├── mongodb_service.py   # MongoDB persistence
│   │   └── portfolio_service.py # Portfolio business logic
│   │
│   ├── models/
│   │   ├── request_models.py    # Pydantic request schemas
│   │   └── response_models.py   # Pydantic response schemas
│   │
│   └── utils/
│       ├── logger.py            # Logging setup
│       └── helpers.py           # Utility functions
│
├── tests/
│   ├── test_agents.py
│   ├── test_graph.py
│   └── test_api.py
│
├── requirements.txt             # Dependencies
├── .env                         # Environment variables
├── run.py                       # Entry point
└── README.md                    # This file
```

---

## Installation

### Prerequisites

- Python 3.9+
- MongoDB (local or remote)
- Groq API Key (for LLM calls)
- Optional: AlphaVantage API Key, NewsAPI Key

### Setup

1. **Clone & Navigate**
   ```bash
   cd investment-advisor-agent
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\Activate.ps1
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Edit .env with your API keys
  GROQ_API_KEY=your_groq_api_key
   MONGODB_URI=mongodb://localhost:27017
   ALPHA_VANTAGE_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   ```

5. **Start MongoDB** (if local)
   ```bash
   mongod
   ```

---

## Running the Application

### Start the API Server

```bash
# Development (with auto-reload)
python run.py

# Or directly
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at: **http://127.0.0.1:8000**

### Interactive API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## API Endpoints

### 1. Main Investment Recommendation

**POST** `/invest`

**Request:**
```json
{
  "user_goal": "Long-term wealth creation for retirement",
  "investment_amount": 50000,
  "duration_years": 5
}
```

**Response:**
```json
{
  "risk_profile": "moderate",
  "portfolio": {
    "NIFTYBEES.NS": 22500.0,
    "JUNIORBEES.NS": 10000.0,
    "GOLDBEES.NS": 10000.0,
    "HDFCBANK.NS": 7500.0
  },
  "critique": "Portfolio approved",
  "workflow_history": [
    {
      "agent": "planner",
      "output": "..."
    },
    {
      "agent": "risk_profiler",
      "output": "moderate"
    }
    // ... more agents
  ]
}
```

### 2. Portfolio History

**GET** `/portfolio-history?limit=10`

Retrieve past portfolio recommendations from MongoDB.

### 3. Rebalancing

**POST** `/rebalance`

```json
{
  "current_portfolio": {"NIFTYBEES.NS": 20000, "GOLDBEES.NS": 10000},
  "target_weights": {"NIFTYBEES.NS": 0.6, "GOLDBEES.NS": 0.4}
}
```

Returns rebalancing actions (buy/sell amounts).

### 4. Health Check

**GET** `/health`

---

## Testing

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest --cov=app tests/
```

---

## Key Features

### 1. **Multi-Agent Workflow**
- Sequential agent execution with state passing
- Conditional routing for critique loop
- Full decision history logging

### 2. **Real Market Data**
- yFinance for Indian stock prices (₹ enabled)
- Live ETF data: Nifty, Gold, Bank indices
- Extensible to global markets

### 3. **Risk-Based Allocation**
- **Low Risk**: 50% Nifty ETF, 30% Gold, 20% Blue Chip
- **Moderate Risk**: 45% Nifty, 20% Next 50, 20% Gold, 15% Blue Chip
- **High Risk**: 35% Nifty, 30% Next 50, 20% Growth, 15% Blue Chip

### 4. **Validation & Critique**
- Diversification checks (min 3 assets)
- Concentration limits (max 60% single position)
- Reflection loop for iterative refinement

### 5. **Persistent Storage**
- MongoDB for portfolio history
- Timestamped records for audit trail
- Historical analysis capabilities

### 6. **Portfolio Rebalancing**
- Monthly drift detection
- Automated rebalancing recommendations
- Executable transaction plan

---

## Configuration

### Environment Variables

```env
# Groq API
GROQ_API_KEY=your_groq_api_key

# Database
MONGODB_URI=mongodb://localhost:27017

# Market Data (Optional)
ALPHA_VANTAGE_KEY=xxxxx
NEWS_API_KEY=xxxxx

# App Settings
DEBUG=True
```

### LLM Models

Currently using **OpenAI GPT OSS 120B via Groq** for optimal cost-performance:
```python
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
```

Set `GROQ_MODEL` in `.env` to use a different Groq-supported model.

---

## Advanced Usage

### 1. Custom Asset Watchlist

Edit `app/tools/market_tools.py`:
```python
WATCHLIST = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consulting",
    "YOUR_TICKER": "Asset Name"
}
```

### 2. Monthly Rebalancing Schedule

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(rebalance_portfolio, "cron", hour=0, day_of_week="mon")
scheduler.start()
```

### 3. News Sentiment Integration

Uncomment in agents/market_research.py to add news analysis:
```python
from app.tools.news_fetcher import fetch_market_news

news = fetch_market_news("nifty 50")
# Analyze sentiment before portfolio construction
```

---

## Performance

### Typical Workflow Execution

| Agent | Duration |
|-------|----------|
| Planner | ~1-2s |
| Risk Profiler | ~1-2s |
| Market Research | ~3-5s |
| Portfolio Builder | <1s |
| Critic | <1s |
| **Total** | **~6-10s** |

*Depends on API latency and network conditions*

### Cost per Request

- Groq LLM: Pricing depends on the selected model and Groq plan
- Market Data (yFinance): Free
- NewsAPI: Free tier (100/day)

---

## Troubleshooting

### MongoDB Connection Failed
```
Error: MongoDB connection failed
Solution: Ensure mongod is running
mongod --dbpath=/path/to/data
```

### Groq API Error
```
Error: Invalid API key
Solution: Check .env file and GROQ_API_KEY
export GROQ_API_KEY="your_groq_api_key"
```

### Market Data Not Available
```
Error: yFinance returned empty data
Solution: Check ticker symbols and market hours
Use "NIFTYBEES.NS" (includes .NS extension)
```

---

## Roadmap

- [ ] Real options pricing (Black-Scholes)
- [ ] Tax-loss harvesting recommendations
- [ ] Multi-currency support
- [ ] Risk Factor analysis (alpha/beta)
- [ ] Backtesting engine
- [ ] Mobile app frontend
- [ ] Graph database for entity relationships
- [ ] Real-time streaming prices

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Documentation**: Read inline code comments
- **Issues**: File a GitHub issue
- **Email**: support@investmentadvisor.local

---

**Built with ❤️ using LangChain & LangGraph**
