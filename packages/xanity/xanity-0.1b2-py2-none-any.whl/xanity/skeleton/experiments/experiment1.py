import xanity

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

def main(
        n_trials=200,
        n_learn_rnds =5,
        train_frac=0.8,
        ):
    
    """ do experiment 1 """
    
    fakevar = [1.3, 3.5, 6.78, -34.51]
    xanity.log("here is a print from experiment 1")
    xanity.save_variable('fakevar', fakevar)

if __name__=='__main__':
    xanity.run_hook()