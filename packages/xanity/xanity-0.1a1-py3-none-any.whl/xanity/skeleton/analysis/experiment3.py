import time

def main(data_dir=None,
         metadata=None):
    if type(data_dir) is list:
        data_dir = data_dir[0]

    with open(pathjoin(data_dir, 'resultsdict.pkl'), 'rb') as f:
        data = pickle.load(f)
