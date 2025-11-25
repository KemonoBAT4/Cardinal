from core.system import cardinal
import sys

possible_args = ["setup", ]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv.pop()
        print(arg)
        if arg == "setup":
            print("Setting up database...")
            cardinal.setup()
        #endif
    #endif
    cardinal.run()
#endif
