import os

import pandas as pd
import random
import itertools

# Define positions and number of trials
positions = ['L', 'LM', 'R', 'RM']
trial_cases = ["absent", "present"]
total_trials = 72
max_present_trials = (72 // 3) * 2
max_absent_trials = 72 // 3
present_to_trial_ration = 2

def generate_all_lines():
    all_lines = []
    for trial in trial_cases:
        for tl in positions:
            for dl in positions:
                line = (trial, tl, dl)
                all_lines.append(line)
                random.shuffle(all_lines)
    return all_lines


def is_next_line_valid(next_line, prev_line=None):
    if next_line[0] == "absent":
        return is_next_absent_valid(next_line, prev_line)
    elif next_line[0] == "present":
        return is_next_present_valid(next_line, prev_line)
    else:
        raise ValueError(f"Trial case {next_line[0]} is incorrect.")


def is_next_absent_valid(next_line, prev_line):
    if prev_line is None:
        return True
    if prev_line[0] == "absent":
        # absent trial was before
        return next_line[1]!=prev_line[1] # return True id TL is not prev TL
    else:
        # present trial was before
        return next_line[1]!=prev_line[1] and next_line[1]!=prev_line[2] # return True if TL is not prev TL or DL


def is_next_present_valid(next_line, prev_line):
    tl, dl = next_line[1], next_line[2]
    if tl == dl:
        return False
    if prev_line is None:
        return True
    p_tl, p_dl = prev_line[1], prev_line[2]
    if prev_line[0] == "absent":
        # absent trial was before
        return tl != p_tl and dl != p_tl
    else:
        # present trial was before
        return tl != p_dl and tl != p_dl and dl != p_tl and dl != p_dl


def generate_all_valid_lines(prev_line=None):
    return [line for line in generate_all_lines() if is_next_line_valid(line, prev_line)]


def create_dataframe(depth, prev_line=None, present_trials=0, absent_trials=0, sequence=None):
    print(depth)
    if sequence is None:
        sequence = []

    if depth == 0:
        # If depth is 0, construct the DataFrame and return it
        df = pd.DataFrame(sequence, columns=['Trial', 'TL', 'DL'])
        df.to_csv("data.csv", index=False)
        return df

    if present_trials >= max_present_trials or absent_trials >= max_absent_trials:
        return None

    results = []
    for p in generate_all_valid_lines(prev_line):
        if p[0] == "absent":
            absent_trials += 1
        elif p[0] == "present":
            present_trials += 1
        else:
            raise ValueError(f"Trial case {p[0]} is not known.")
        sub_results = create_dataframe(depth - 1, p, present_trials, absent_trials, sequence + [p])
        if sub_results is not None:
            return sub_results


if __name__ == "__main__":
    # Call create_dataframe with depth 3
    result = create_dataframe(depth=72)

    # Convert the result to a DataFrame for better visualization
    df = pd.DataFrame(result, columns=["Trial", "TL", "DL"])

    folder_path = "data"
    file_name = "data_2.csv"
    file_path = os.path.join(folder_path, file_name)

    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)
