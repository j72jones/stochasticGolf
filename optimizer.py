import pandas as pd
import numpy as np

data = pd.read_csv("hole_12_data/hole_12_markov_states.csv")

def simulate_shot(x,y,club,theta, count):
    pass
    return [(0,0) for _ in range(count)]


"""
Data in form
X|Y|Z|fairway|green
...

With 2 extra points

start = (x,y)
hole = (x,y)
and a green polygon

Green polygon, we apply a log(d+1)+1 scale where d is the distance from the hole for "how difficult"

Filter data for only state that have some fairway
Markov chain has 2 states for each fairway state (1 standard state and 1 feeder state for drops)
Need to decide how to deal with the green (absorbing state)
"""

# teebox = (34°04'48"N 84°13'40"W)
# flag = (34°04'47"N 84°13'26"W)


def optimize_chain(state_df, flag):
    state_df["flag distance"] = np.sqrt((state_df['x'] - flag[0])**2 + (state_df['y'] - flag[1])**2)
    state_df["green_rate"] = np.where(state_df["green"] > 0, np.log(state_df["flag distance"] + 1) + 1, 0) + np.where((state_df["green"] <= 0) & (state_df["flag distance"] <= 60), np.log(state_df["flag distance"] + 1) + 1, 0)

    len(state_df["green_rate"] == 0)

    markov_chain = np.zeros(shape=(len(state_df) + len(state_df["green_rate"] == 0)))

    