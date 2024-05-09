import importlib
import pathlib
import sys


def main():
    PATH_ROOT = pathlib.Path(__file__).parent.parent
    sys.path[0] = str(PATH_ROOT)
    import pyboiler

    print(pyboiler.dir())

    logging = pyboiler.logging.


if __name__ == "__main__":
    main()
