import numpy as np
import pandas as pd
from collections import defaultdict, deque

# dataframes imported from data folder
teams = pd.read_csv("data/MTeams.csv")
seeds = pd.read_csv("data/MNCAATourneySeeds.csv")
srs = pd.read_csv("data/MNCAATourneySeedRoundSlots.csv")

# retrieves team id by seed in a given year
def get_id_by_seed(year, seed):
    return seeds.query("Season == @year and Seed == @seed")["TeamID"].item()

# retrieves team name by ID
def get_name_by_id(id):
    return teams.loc[teams["TeamID"] == id, "TeamName"].item()

# retrieves team name by seed in a given year
def get_name_by_seed(year, seed):
    return get_name_by_id(get_id_by_seed(year, seed))

# retrieves list of seeds in the given year
def get_seeds_by_year(year):
    return seeds.loc[seeds['Season'] == year, 'Seed'].values

# predicts winning team (currently seed based)
def predict_winner(year, seed_a, seed_b):
    seed_val_a = ''.join(c for c in seed_a if c.isdigit())
    seed_val_b = ''.join(c for c in seed_b if c.isdigit())
    return seed_a if int(seed_val_a) <= int(seed_val_b) else seed_b

# constructs a bracket using the seeds in a given year
def build_bracket(year):
    seeds = get_seeds_by_year(year)
    bracket = defaultdict(list)
    first_four = defaultdict(list)

    # insert First Four matches
    for seed in seeds:
        round_zero = srs.query("Seed == @seed and GameRound == 0")
        if round_zero.empty:
            round_one = srs.query("Seed == @seed and GameRound == 1")
            bracket[round_one["GameSlot"].item()].append(seed)
        else:
            first_four[round_zero["GameSlot"].item()].append(seed)

    # admit winners of First Four to the first round
    for slot in first_four:
        team_a, team_b = first_four[slot]
        winner = predict_winner(year, team_a, team_b)
        round_one = srs.query("Seed == @winner and GameRound == 1")
        bracket[round_one["GameSlot"].item()].append(winner)

    # level order traversal to fill up bracket
    queue = deque(slot for slot in bracket)
    curr_round = 1
    while queue and curr_round < 6:
        # number of matches in the current round
        num_slots = len(queue)
        
        for _ in range(num_slots):
            slot = queue.popleft()
            team_a, team_b = bracket[slot]

            winner = predict_winner(year, team_a, team_b)
            next_round = srs.query("Seed == @winner and GameRound == @curr_round + 1")
            next_slot = next_round["GameSlot"].item()
            
            if next_slot not in bracket:
                queue.append(next_slot)

            bracket[next_slot].append(winner)

        curr_round += 1
    
    return bracket

if __name__ == "__main__":
    print('Bracket for 2024 (seed-only calculation)')
    print('----------------------------------------')

    bracket2024 = build_bracket(2024)
    for slot in bracket2024:
        teams2024 = [get_name_by_seed(2024, seed) for seed in bracket2024[slot]]
        print(f"{slot}: {teams2024[0]} vs {teams2024[1]}")
