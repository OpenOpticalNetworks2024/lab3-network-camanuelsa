import pandas as pd
from pathlib import Path
from core.math_utils import *
from core.elements import *

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'
network = Network(file_input) # create the network object
network.connect() # connect the network
paths_data = [] # initialize the paths data list
for src in network.nodes: # start of the path (source)
    for dst in network.nodes: # end of the path (destination)
        if src != dst: # control to ensure that the start and the end are not the same
            paths = network.find_paths(src, dst) # all paths from start to end
            for path in paths: # working one path at time
                path_string = '->'.join(path) # creating the string of the path as A->B_>...
                signal = network.propagate(Signal_information(1e-3, path)) # propagating the signal from start to end and uptade its information
                total_latency = signal.latency # latency of the signal along the path
                total_noise = signal.noise_power # noise of the signal along the path
                snr_db = lin2db(signal.signal_power / total_noise) # SNR of the signal along the path
                paths_data.append({ # adding the path information to the paths data list
                    'Path': path_string,
                    'Total Latency (s)': total_latency,
                    'Total Noise (W)': total_noise,
                    'SNR (dB)': snr_db
                })
df = pd.DataFrame(paths_data) # transform the list of paths data into a panda dataframe
csv_path = ROOT / 'weighted_path.csv'
df.to_csv(csv_path, index=False) # report on an csv file the dataframe
network.draw() # draw the network and export a png of it
print(f"Results saved to {csv_path}")


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
