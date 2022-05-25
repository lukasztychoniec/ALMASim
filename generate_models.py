import utils
import argparse

parser =argparse.ArgumentParser()
parser.add_argument("data_dir", type=str, 
        help='The directory in wich the simulated model cubes are stored;')
parser.add_argument("csv_name", type=str, 
        help='The name of the .csv file in which to store the simulated source parameters;')
parser.add_argument('n', type=int, help='The number of cubes to generate;')
args = parser.parse_args()

utils.generate_cubes(**vars(args))