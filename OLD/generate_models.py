import utils
import argparse
import time

parser =argparse.ArgumentParser()
parser.add_argument("data_dir", type=str, 
        help='The directory in wich the simulated model cubes are stored;')
parser.add_argument("csv_name", type=str, 
        help='The name of the .csv file in which to store the simulated source parameters;')
parser.add_argument('n', type=int, help='The number of cubes to generate;')
args = parser.parse_args()
start = time.time()
utils.generate_cubes(**vars(args))
print(f'Execution took {time.time() - start} seconds')
