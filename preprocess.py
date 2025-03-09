import pandas as pd
import numpy as np

# Load datasets
teams = pd.read_csv("data/MTeams.csv")
seeds = pd.read_csv("data/MNCAATourneySeeds.csv")
results = pd.read_csv("data/MNCAATourneyDetailedResults.csv")

# Extract year, team seeds, and results
seeds["SeedValue"] = seeds["Seed"].str.extract(r'(\d+)').astype(int)
results = results[['Season', 'WTeamID', 'LTeamID']]

# Merge seeds with results
results = results.merge(seeds[['Season', 'TeamID', 'SeedValue']], 
                        left_on=['Season', 'WTeamID'], 
                        right_on=['Season', 'TeamID'], 
                        how='left').rename(columns={'SeedValue': 'WSeed'})
results.drop(columns=['TeamID'], inplace=True)

results = results.merge(seeds[['Season', 'TeamID', 'SeedValue']], 
                        left_on=['Season', 'LTeamID'], 
                        right_on=['Season', 'TeamID'], 
                        how='left').rename(columns={'SeedValue': 'LSeed'})
results.drop(columns=['TeamID'], inplace=True)

# Feature engineering
results['SeedDiff'] = results['WSeed'] - results['LSeed']

# Create target variable (1 if WTeam wins, 0 otherwise)
data = pd.DataFrame({
    'TeamA': results['WTeamID'],
    'TeamB': results['LTeamID'],
    'SeedDiff': results['SeedDiff'],
    'Result': 1  # Team A wins
})

# Add losing matchups as well (reverse teams)
reverse_data = pd.DataFrame({
    'TeamA': results['LTeamID'],
    'TeamB': results['WTeamID'],
    'SeedDiff': -results['SeedDiff'],
    'Result': 0  # Team A loses
})

data = pd.concat([data, reverse_data])

# Save processed data
data.to_csv("data/processed_results.csv", index=False)

print("Data preprocessing complete. Saved as processed_results.csv")
