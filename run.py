
from core.system.cardinal import Cardinal
import sys

from core.configs import *

if __name__ == '__main__':

    args: list = sys.argv.copy()

    test = args.pop(0) # run.py
    name = args.pop(0) # name

    cardinal = Cardinal(name=name)

    run_arg = args.pop(0)

    if run_arg == "setup":
        print("Setting up database...")
        cardinal.setup()
    else:
        cardinal.run()
    #endif
#endif
