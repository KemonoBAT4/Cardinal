
from core.system.cardinal import Cardinal
import configparser

config = configparser.ConfigParser()
config.read("application.cfg")

Cardinal = Cardinal(config=config)

if __name__ == "__main__":
    Cardinal.start()
#endif

