import pandas as pd
from fuzzywuzzy import process

# This script cleans and standardizes fund categories from fund rankings.csv dataset using fuzzy matching. It normalizes the casing and whitespace of fund categories, maps them to a set of known categories, and saves the cleaned data to cleaned_fund_rankings.csv
# Load dataset
df = pd.read_csv("funds/management/csv_data/fund_rankings.csv")

# Normalize casing and strip whitespace
df['Fund_Category'] = df['Fund_Category'].str.strip().str.lower()

# Define the target categories and their canonical labels
known_categories = {
    'Income Fund': 'Fixed Income Funds',
    'Bond Fund': 'Fixed Income Funds',
    'Equity Fund': 'Large Cap Equity Funds',
    'Growth Fund': 'REITs and/or Infrastructure Funds',
    'Ethical Fund': 'REITs and/or Infrastructure Funds',
    'Real Estate Fund': 'REITs and/or Infrastructure Funds',
    'Infrastructure Fund': 'REITs and/or Infrastructure Funds',
    'Cash/Money Market Fund': 'Cash/Money Market Funds',
}

# Fuzzy match each fund category to the known categories
def map_category(cat):
    match, score = process.extractOne(cat, known_categories.keys())
    if score >= 85:  # confident match threshold
        return known_categories[match]
    return cat.title()  # fallback to cleaned but unmapped category

# Apply fuzzy matching and mapping
df['Fund_Category'] = df['Fund_Category'].apply(map_category)

# Save the cleaned dataset
df.to_csv("funds/management/csv_data/cleaned_fund_rankings.csv", index=False)
print("Fuzzy-matched and cleaned data saved to 'funds/management/csv_data/cleaned_fund_rankings.csv'")
