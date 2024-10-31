import re
import json

# Sample chat transcript
chat = """
4:20 PM Kemi: Chinedu, need to move on USD/NGN. What’s your rate?
4:21 PM Chinedu: Kemi, good to hear from you. I can offer 775.50. How much are you looking to trade?
4:22 PM Kemi: Looking to push through $3 million. But 775.50 isn’t going to work. I need better.
4:23 PM Chinedu: $3 million, okay. But Kemi, the market’s tight right now. 775.50 is competitive. How about 775 flat? That’s me squeezing it.
4:24 PM Kemi: Chinedu, you and I both know there’s some room to maneuver here. 774.80, and I’ll confirm it right now.
4:25 PM Chinedu: 774.80 is below where I’m comfortable, Kemi. Best I can stretch to is 774.90. That’s final.
4:26 PM Kemi: 774.90, huh? Alright, you’ve got a deal. Let’s lock it in for $3 million at 774.90. Get the paperwork sorted ASAP.
4:27 PM Chinedu: Done. I’ll have everything over to you within the hour. Usual settlement, T+2?
4:28 PM Kemi: Yes, T+2. Appreciate the quick turnaround, Chinedu. Let’s make this smooth.
4:29 PM Chinedu: You got it, Kemi. We’ll get it done.
"""

# Initialize structured data
structured_data = {
    "Currency Pair": None,
    "Amount": None,
    "Bid Price": None,
    "Ask Price": None,
    "Agreed Rate": None,
    "Settlement Date": None,
    "Events": []
}

# Define regex patterns
currency_pair_pattern = r'\b(USD/NGN)\b'
amount_pattern = r'\$(\d+\.?\d*) million'
rate_pattern = r'(\d+\.\d+)'
settlement_pattern = r'T\+(\d+)'

# Extract currency pair
currency_pair_match = re.search(currency_pair_pattern, chat)
if currency_pair_match:
    structured_data["Currency Pair"] = currency_pair_match.group(1)

# Extract amount
amount_match = re.search(amount_pattern, chat)
if amount_match:
    structured_data["Amount"] = f"{amount_match.group(1)} million"

# Extract rates (offer, bid, and agreed)
rates = re.findall(rate_pattern, chat)
if rates:
    structured_data["Ask Price"] = rates[0]  # Chinedu's offer rate
    structured_data["Bid Price"] = rates[2]  # Kemi's counteroffer
    structured_data["Agreed Rate"] = rates[3]  # Final agreed rate

# Extract settlement date
settlement_match = re.search(settlement_pattern, chat)
if settlement_match:
    structured_data["Settlement Date"] = f"T+{settlement_match.group(1)}"

# Record events for relationships
structured_data["Events"] = [
    {"Propose Trade": "Kemi proposes a trade of USD/NGN."},
    {"Offer Rate": f"Chinedu offers a rate of {structured_data['Ask Price']}."},
    {"Counteroffer": f"Kemi counters with a rate of {structured_data['Bid Price']}."},
    {"Agree to Rate": f"Chinedu agrees to the rate of {structured_data['Agreed Rate']}."},
    {"Confirm Trade": f"Kemi confirms the trade at {structured_data['Agreed Rate']}."}
]

# Convert to JSON for structured format
structured_json = json.dumps(structured_data, indent=4)
print(structured_json)
