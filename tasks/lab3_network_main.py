import pandas as pd
from pathlib import Path
from core.math_utils import *
from core.elements import *

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'
network = Network(file_input)
network.connect()
paths_data = []
for src in network.nodes:
    for dst in network.nodes:
        if src != dst:
            paths = network.find_paths(src, dst)
            for path in paths:
                path_string = '->'.join(path)
                signal = network.propagate(Signal_information(1e-3, path))
                total_latency = signal.latency
                total_noise = signal.noise_power
                snr_db = lin2db(signal.signal_power / total_noise)
                paths_data.append({
                    'Path': path_string,
                    'Total Latency (s)': total_latency,
                    'Total Noise (W)': total_noise,
                    'SNR (dB)': snr_db
                })
df = pd.DataFrame(paths_data)
csv_path = ROOT / 'weighted_path.csv'
df.to_csv(csv_path, index=False)
network.draw()
print(f"Results saved to {csv_path}")


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
