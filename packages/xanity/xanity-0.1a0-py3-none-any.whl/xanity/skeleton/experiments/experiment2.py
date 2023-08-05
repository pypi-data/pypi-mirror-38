import time

savepath = []
mylogger = []

EXPERIMENT_PARAMETERS = {
}

# define the location and format of data storage for use by data-processing scripts:
DATA_DEFINITION = {
    'datafile': 'progress.csv',
    'DictReader': True,
    'delimiter': ',',
    'rowtest': lambda row:
    len(row) == 6 and row['episode number'].strip(', ').isdigit() and row['episode reward'].dtype == 'float64',
    'rowdata': lambda row: (int(row['episode number'].strip(' ,')), float(row['episode reward'].strip(' ,')))
}


def main(metadata=None,
        n_trials=200,
        n_learn_rnds =5,
        train_frac=0.8,
):
  
  global savepath, mylogger
  savepath = metadata['status']['savepath']
  mylogger = metadata['logger']
  
  # do experiment 1
  print("here is a print from experiment 2")
