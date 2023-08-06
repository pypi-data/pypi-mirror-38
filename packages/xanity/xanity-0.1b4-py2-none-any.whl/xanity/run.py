#!/usr/bin/env python

from __future__ import print_function
import sys

def main():
    """
        look in experiments folder and run all or passed selection
    """
    from xanity import xanity
    
    if xanity.args.analyze_only:
        xanity.run_analyses.main()

    else:
        xanity.run_prelude()
        xanity.run_all_exps()
        
        # analyze successful experiments
        if xanity.args.and_analyze:
            for exp in xanity.experiments_of_interest:
                if any(xanity.experiments[exp]['success']):
                    xanity.run_one_analysis(exp)

          #      for i, datadir in enumerate(xanity.experiments[exp]['data_dirs']):
          #          if xanity.experiments[exp]['success'][i]:
          #            #process.main(metadata=metadata)
          #            break
          #            analyze.main()

if __name__ == '__main__':
    main(sys.argv)