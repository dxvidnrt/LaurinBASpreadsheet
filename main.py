import pandas as pd
import random
import itertools

# Define positions and number of trials
positions = ['L', 'LM', 'R', 'RM']
total_trials = 72
present_trials = total_trials * 2 // 3
absent_trials = total_trials - present_trials


def generate_all_present_pairs(prev_pair):
    positions = ['L', 'LM', 'R', 'RM']
    all_pairs = []

    # Generate all possible pairs
    for tl in positions:
        for dl in positions:
            if tl != dl and tl != prev_pair[1] and tl != prev_pair[0] and dl != prev_pair[0] and dl != prev_pair[1]:
                all_pairs.append((tl, dl))

    if len(all_pairs) == 0:
        print("Couldnt generate a present pair.")
    return all_pairs


def generate_unequal_tl_dl_pairs():
    positions = ['L', 'LM', 'R', 'RM']

    # Generate all possible pairs of TL and DL that are unequal
    all_pairs = list(itertools.permutations(positions, 2))

    return all_pairs

def generate_all_absent_pairs(prev_pair)


# Example usage:
prev_pair = ('L', 'RM')  # Example of previous pair
all_pairs = generate_all_pairs(prev_pair)
print(all_pairs)


def generate_unequal_tl_dl_pair():
    positions = ['L', 'LM', 'R', 'RM']
    tl = random.choice(positions)
    dl = random.choice(positions)

    while dl == tl:
        dl = random.choice(positions)

    return tl, dl


def generate_present_pair(pair):

    tl = pair[0]
    dl = pair[1]
    return (tl is not dl)


def generate_present(prev_pair):
    if prev_pair is None:
        present_pair = generate_unequal_tl_dl_pair()
        return "present", present_pair[0], present_pair[1]


    return "present", random.choice(positions)


# Function to generate TL and DL pairs
def generate_pairs(prev_pair=None):
    tl = random.choice(positions)
    dl = random.choice(positions)

    if prev_pair is not None:
        while dl == tl or dl == prev_pair[0] or dl == prev_pair[1]:
            dl = random.choice(positions)

    return tl, dl


# Generate TL and DL pairs for present trials
present_pairs = []
prev_pair = None
for _ in range(present_trials):
    tl, dl = generate_pairs(prev_pair)
    present_pairs.append((tl, dl))
    prev_pair = (tl, dl)

# Generate TL and DL pairs for absent trials
absent_pairs = []
for _ in range(absent_trials):
    tl, dl = generate_pairs()
    absent_pairs.append((tl, dl))

# Create DataFrame
df = pd.DataFrame(present_pairs + absent_pairs, columns=['TL', 'DL'])
df['Condition'] = ['present'] * present_trials + ['absent'] * absent_trials

# Shuffle DataFrame
df = df.sample(frac=1).reset_index(drop=True)

# Ensure each position appears 18 times as TL and DL
position_counts = df['TL'].value_counts()
for position in positions:
    if position_counts.get(position, 0) < 18:
        missing_count = 18 - position_counts.get(position, 0)
        for _ in range(missing_count):
            idx = df[df['TL'] != position].sample().index
            df.at[idx, 'TL'] = position

position_counts = df['DL'].value_counts()
for position in positions:
    if position_counts.get(position, 0) < 18:
        missing_count = 18 - position_counts.get(position, 0)
        for _ in range(missing_count):
            idx = df[df['DL'] != position].sample().index
            df.at[idx, 'DL'] = position

print(df)
