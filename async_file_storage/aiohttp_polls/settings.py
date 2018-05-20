import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent

def get_config(path):
	with open(path) as f:
		config = yaml.load(f)
	return config

