import os
import uuid
import pandas as pd
import random
import math
import itertools

# Define positions and number of trials
positions = ['L', 'LM', 'R', 'RM']
trial_cases = ["absent", "present"]
total_trials = 72
max_present_trials = math.ceil((total_trials / 3) * 2)
max_absent_trials = math.ceil(total_trials / 3)
present_to_trial_ration = 2
folder_path = "data"


def generate_all_lines():
    random.shuffle(trial_cases)
    random.shuffle(positions)
    for trial in trial_cases:
        for tl in positions:
            random.shuffle(positions)
            for dl in positions:
                yield trial, tl, dl


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
        return next_line[1] != prev_line[1]  # return True id TL is not prev TL
    else:
        # present trial was before
        return next_line[1] != prev_line[1] and next_line[1] != prev_line[2]  # return True if TL is not prev TL or DL


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
    for line in generate_all_lines():
        if is_next_line_valid(line, prev_line):
            yield line


def sort_by_trial(lines, present, absent, present_to_trial_ratio=1.0):
    present_buffer = []
    absent_buffer = []
    random_ratio = 0.66

    def yield_from_buffers():
        nonlocal present_buffer, absent_buffer
        if present >= absent * present_to_trial_ratio:
            while absent_buffer or present_buffer:
                if absent_buffer and random.random() < random_ratio:
                    yield absent_buffer.pop(0)
                elif present_buffer:
                    yield present_buffer.pop(0)
        else:
            while absent_buffer or present_buffer:
                if present_buffer and random.random() < random_ratio:
                    yield present_buffer.pop(0)
                elif absent_buffer:
                    yield absent_buffer.pop(0)

    for line in lines:
        if line[0] == "present":
            present_buffer.append(line)
        else:
            absent_buffer.append(line)

        yield from yield_from_buffers()

    yield from yield_from_buffers()  # Ensure any remaining buffered items are yielded


def create_dataframe(depth, prev_line=None, sequence=None, present_trials=0, absent_trials=0, ):
    print(f"Depth: {depth}")
    if absent_trials != 0:
        print(f"Present to Absent nominated: {present_trials / (absent_trials * present_to_trial_ration)}")
    if sequence is None:
        sequence = []

    if depth == 0:
        # If depth is 0, construct the DataFrame and return it
        df = pd.DataFrame(sequence, columns=['Trial', 'TL', 'DL'])
        file_name = f"data_{uuid.uuid4()}.csv"
        file_path = os.path.join(folder_path, file_name)
        df.to_csv(file_path, index=False)
        return

    if present_trials > max_present_trials or absent_trials > max_absent_trials:
        print(f"Present: {present_trials}, Absent: {absent_trials}")
        return

    for p in sort_by_trial(generate_all_valid_lines(prev_line), present_trials, absent_trials):
        create_dataframe(depth - 1, p, sequence + [p], present_trials+int(p[0] == "present"), absent_trials+
                         int(p[0] == "absent"))


if __name__ == "__main__":
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Call create_dataframe with depth 3
    create_dataframe(depth=total_trials)

