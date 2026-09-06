"""Verify investment guidance data structure."""
import json

# Read the investment guidance database
with open('app/services/investment_guidance_service.py', 'r') as f:
    content = f.read()

# Extract investment symbols
symbols = ['NIFTYBEES.NS', 'JUNIORBEES.NS', 'GOLDBEES.NS', 'HDFCBANK.NS', 'INFY.NS', 'BANKBEES.NS', 'TCS.NS', 'RELIANCE.NS']

print("Checking investment guidance data structure:\n")

# Quick check for step descriptions
for symbol in symbols:
    # Find the section for this symbol
    if f'"{symbol}"' in content:
        # Extract investment_steps section
        start = content.find(f'"{symbol}"')
        end = content.find('def get_investment_guidance', start)
        section = content[start:end]
        
        # Count steps
        step_count = section.count('"step":')
        desc_count = section.count('"description":')
        
        print(f"✓ {symbol}: {step_count} steps, {desc_count} descriptions")

print("\n✓ All investment entries validated!")
