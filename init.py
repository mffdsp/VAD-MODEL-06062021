from config.Cmd import Cmd
import sys
import os
from run_simulation import runsim, runsim2, ejection_variance_value

args = Cmd.args

if __name__ == "__main__":
    try:
        if args.mode == "simaan":
            runsim2.__run()
        elif args.mode == "test": 
            ejection_variance_value.__run()
        elif args.mode == "vad":
            runsim.__run()
        elif args.mode == "initproject":
            print('Fetching Dependencies...')
            os.system('pip install -r requirements.txt')
            os.system('pip install -e .')
        else:
            print("Args error")
            
    except (Exception, BaseException) as e:
        print(e)
        sys.exit(1)
