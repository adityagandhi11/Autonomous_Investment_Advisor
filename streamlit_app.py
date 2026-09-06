"""Streamlit UI for Autonomous Investment Advisor."""

import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Investment Advisor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("⚙️ Configuration")
api_base_url = st.sidebar.text_input(
    "API Base URL",
    value="http://127.0.0.1:8000",
    help="FastAPI server URL"
)

# Main title
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1>🤖 AI Investment Advisor</h1>
    <p style="color: #666; font-size: 18px;">
        Multi-Agent AI System for Personalized Investment Recommendations
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Input Section
st.subheader("📋 Investment Details")
col1, col2, col3 = st.columns(3)

with col1:
    investment_goal = st.text_area(
        "Investment Goal",
        value="I want to invest for long-term wealth creation",
        height=80,
        help="What is your investment objective?"
    )

with col2:
    investment_amount = st.number_input(
        "Investment Amount (₹)",
        value=50000,
        min_value=1000,
        step=1000,
        help="How much capital are you investing?"
    )

with col3:
    duration_years = st.number_input(
        "Investment Horizon (Years)",
        value=5,
        min_value=1,
        max_value=50,
        step=1,
        help="For how many years?"
    )

st.divider()

# Submit Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    analyze_button = st.button(
        "🚀 ANALYZE PORTFOLIO",
        use_container_width=True,
        type="primary"
    )

# State management
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# Analyze button logic
if analyze_button:
    st.session_state.is_loading = True
    
    # Show loading state
    with st.spinner("🔄 Running multi-agent workflow..."):
        try:
            # Call FastAPI backend
            response = requests.post(
                f"{api_base_url}/invest",
                json={
                    "user_goal": investment_goal,
                    "investment_amount": float(investment_amount),
                    "duration_years": int(duration_years)
                },
                timeout=120
            )
            
            if response.status_code == 200:
                st.session_state.analysis_result = response.json()
                st.session_state.is_loading = False
                st.success("Portfolio analysis complete!")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                st.session_state.is_loading = False
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {api_base_url}. Is the server running?")
            st.session_state.is_loading = False
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.is_loading = False

# Display Results
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    st.divider()
    
    # Agent Execution Trace
    st.subheader("Agent Execution Trace")
    
    trace_cols = st.columns(5)
    agents = ["Planner", "Risk Profiler", "Market Research", "Portfolio Builder", "Critic"]
    
    for idx, (col, agent) in enumerate(zip(trace_cols, agents)):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: #e8f5e9; border-radius: 8px;">
                <div style="font-size: 24px;">✓</div>
                <div style="font-size: 12px; font-weight: bold;">{agent}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Arrow between agents
        if idx < len(agents) - 1:
            st.markdown("<div style='text-align: center; font-size: 20px;'>↓</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Risk Assessment Section
    st.subheader("AI Risk Assessment")
    
    risk_profile = result.get("risk_profile", "N/A").upper()
    risk_colors = {
        "LOW": "#4CAF50",
        "MODERATE": "#FF9800",
        "HIGH": "#F44336"
    }
    risk_color = risk_colors.get(risk_profile, "#9E9E9E")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: {risk_color}; color: white; border-radius: 10px;">
        <div style="font-size: 32px; font-weight: bold;">{risk_profile} RISK</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Portfolio Allocation Section
    st.subheader("📊 Recommended Portfolio Allocation")
    
    portfolio = result.get("portfolio", {})
    
    if portfolio:
        total_portfolio_value = sum(
            allocation if isinstance(allocation, (int, float))
            else allocation.get("amount", 0)
            for allocation in portfolio.values()
        )

        def allocation_details(allocation):
            if isinstance(allocation, (int, float)):
                amount = allocation
                percentage = (amount / total_portfolio_value * 100) if total_portfolio_value else 0
                return percentage, amount
            return allocation.get("percentage", 0), allocation.get("amount", 0)

        # Create pie chart
        labels = []
        values = []
        amounts = []
        
        for asset, allocation in portfolio.items():
            labels.append(asset)
            percentage, amount = allocation_details(allocation)
            values.append(percentage)
            amounts.append(amount)
        
        # Plotly pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            textposition='inside',
            textinfo='label+percent',
            marker=dict(
                colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
            ),
            hovertemplate='<b>%{label}</b><br>%{value}%<extra></extra>'
        )])
        
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Table view
        st.markdown("**Allocation Details:**")
        col1, col2, col3 = st.columns(3)
        
        for idx, (asset, allocation) in enumerate(portfolio.items()):
            if idx % 3 == 0:
                col = col1
            elif idx % 3 == 1:
                col = col2
            else:
                col = col3
            
            with col:
                percentage, amount = allocation_details(allocation)
                st.metric(
                    label=asset,
                    value=f"₹{amount:,.0f}",
                    delta=f"{percentage}%"
                )
    
    st.divider()
    
    # Market Research Section
    st.subheader("Market Research Data")
    
    research_data = result.get("research_data", {})
    if research_data:
        with st.expander("Market Snapshot", expanded=False):
            assets = research_data.get("assets", research_data) if isinstance(research_data, dict) else {}
            news = research_data.get("news", {}) if isinstance(research_data, dict) else {}
            if isinstance(assets, dict):
                for ticker, data in assets.items():
                    if isinstance(data, dict):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(ticker, data.get("name", "N/A"))
                        with col2:
                            st.metric("Price", f"₹{data.get('price', 0):.2f}")
                        with col3:
                            monthly_return = data.get("monthly_return_pct", 0)
                            st.metric(
                                "1M Return",
                                f"{monthly_return:.2f}%",
                                delta=f"{monthly_return:.2f}%"
                            )
                    st.divider()
            articles = news.get("articles", []) if isinstance(news, dict) else []
            if articles:
                st.markdown("**Recent News:**")
                for article in articles[:5]:
                    if isinstance(article, dict):
                        st.write(article.get("title", "Untitled article"))
    else:
        st.info("No market research data available")
    
    st.divider()
    
    # Critic Analysis Section
    st.subheader("Critic Analysis")
    
    critique = result.get("critique", "No critique available")
    approved = result.get("approved", False)
    
    approval_badge = "✅ APPROVED" if approved else "⚠️ REQUIRES REVISION"
    approval_color = "#4CAF50" if approved else "#FF9800"
    
    st.markdown(f"""
    <div style="padding: 15px; background: {approval_color}; color: white; border-radius: 8px; margin-bottom: 10px;">
        <b>{approval_badge}</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Feedback:** {critique}")
    
    st.divider()
    
    # Workflow History Section
    st.subheader("Workflow Execution History")
    
    history = result.get("workflow_history", [])
    if history:
        with st.expander("View detailed execution steps", expanded=False):
            for idx, step in enumerate(history, 1):
                st.markdown(f"**Step {idx}:**")
                if isinstance(step, dict):
                    for key, value in step.items():
                        st.markdown(f"- **{key}:** {value}")
                else:
                    st.markdown(f"- {step}")
                st.divider()
    
    # Export Section
    st.divider()
    st.subheader("Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        json_str = json.dumps(result, indent=2, default=str)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        st.info("Portfolio has been saved to MongoDB database")

else:
    # No results yet - show demo info
    if not st.session_state.is_loading:
        st.info("""
        👆 **Get Started:**
        1. Enter your investment goal and amount
        2. Select your investment horizon
        3. Click "ANALYZE PORTFOLIO" to run the multi-agent workflow
        
        The system will:
        - 🧠 Analyze your investment goal
        - 📊 Profile your risk tolerance
        - 📈 Research market opportunities
        - 🎯 Build a personalized portfolio
        - 🧐 Validate diversification
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
    <p>Multi-Agent Investment Advisory System v1.0</p>
</div>
""", unsafe_allow_html=True)
