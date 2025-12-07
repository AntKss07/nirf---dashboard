
import pandas as pd
import json

# Load the temporary combined CSV
combined_df = pd.read_csv('nirf_2025_temp_combined.csv')

# Load the institute-state mapping
with open('institute_state_map.json', 'r', encoding='utf-8') as f:
    institute_state_map = json.load(f)

# Add 'State' column
# Use .get() with a default value (e.g., None) for institutes not found in the map
combined_df['State'] = combined_df['Name'].apply(lambda x: institute_state_map.get(x, None))

# Define the state to region mapping
STATE_TO_REGION_MAP = {
    # North
    "Jammu and Kashmir": "North",
    "Ladakh": "North",
    "Himachal Pradesh": "North",
    "Punjab": "North",
    "Haryana": "North",
    "Delhi": "North",
    "Uttar Pradesh": "North",
    "Uttarakhand": "North",
    "Rajasthan": "North",
    "Chandigarh": "North", # Added Chandigarh

    # South
    "Tamil Nadu": "South",
    "Kerala": "South",
    "Karnataka": "South",
    "Andhra Pradesh": "South",
    "Telangana": "South",
    "Puducherry": "South",

    # East
    "West Bengal": "East",
    "Odisha": "East",
    "Bihar": "East",
    "Jharkhand": "East",

    # West
    "Maharashtra": "West",
    "Gujarat": "West",
    "Goa": "West",
    "Dadra and Nagar Haveli and Daman and Diu": "West",

    # North East
    "Assam": "North East",
    "Arunachal Pradesh": "North East",
    "Manipur": "North East",
    "Meghalaya": "North East",
    "Mizoram": "North East",
    "Nagaland": "North East",
    "Sikkim": "North East",
    "Tripura": "North East",

    # Central
    "Madhya Pradesh": "Central",
    "Chhattisgarh": "Central",

    # Other UTs not explicitly North/South
    "Andaman and Nicobar Islands": "Other",
    "Lakshadweep": "Other",
}

# Function to map state to region
def map_state_to_region(state):
    if state in STATE_TO_REGION_MAP:
        return STATE_TO_REGION_MAP[state]
    else:
        # If a state is not found in the explicit North/South/East/West/North East/Central, assign 'Other'
        return "Other"

# Add 'Region' column
combined_df['Region'] = combined_df['State'].apply(map_state_to_region)

# Reorder columns as specified by the user: Rank, Institute_ID, Name, Score, Category, State, Region
final_columns = ['Rank', 'Institute_ID', 'Name', 'Score', 'Category', 'State', 'Region']
# Ensure all columns exist before reordering, fill missing with None or a default if necessary
for col in final_columns:
    if col not in combined_df.columns:
        combined_df[col] = None
combined_df = combined_df[final_columns]

# Save the final combined DataFrame
combined_df.to_csv('nirf_2025_combined.csv', index=False)

print("Final combined CSV 'nirf_2025_combined.csv' created successfully with State and Region columns.")
print(f"Total rows: {len(combined_df)}")
print("Columns:", combined_df.columns.tolist())
print("\nInstitutes for which state could not be determined (will have 'None' in State column):")
print(combined_df[combined_df['State'].isnull()]['Name'].tolist())
