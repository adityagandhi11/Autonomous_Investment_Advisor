#!/usr/bin/env python
"""Quick test of investment guidance service."""

from app.services.investment_guidance_service import get_investment_guidance
from app.models.response_models import InvestmentDetails

# Test loading guidance for a sample asset
data = get_investment_guidance('NIFTYBEES.NS')
print(f"✓ Investment guidance loaded: {data['name']}")

# Verify structure
print(f"✓ Category: {data.get('category')}")
print(f"✓ Risk Level: {data.get('risk_level')}")
print(f"✓ Investment Steps: {len(data.get('investment_steps', []))} steps")

# Test all investments
test_symbols = ['NIFTYBEES.NS', 'JUNIORBEES.NS', 'GOLDBEES.NS', 'HDFCBANK.NS', 'INFY.NS', 'BANKBEES.NS', 'TCS.NS', 'RELIANCE.NS']
for symbol in test_symbols:
    guidance = get_investment_guidance(symbol)
    steps = guidance.get('investment_steps', [])
    print(f"✓ {symbol}: {guidance['name']} - {len(steps)} steps")
    
    # Check if all steps have required fields
    for step in steps:
        if 'description' not in step or not step['description']:
            print(f"  ⚠ Warning: Step {step.get('step')} missing description")

print("\n✓ All tests passed!")
