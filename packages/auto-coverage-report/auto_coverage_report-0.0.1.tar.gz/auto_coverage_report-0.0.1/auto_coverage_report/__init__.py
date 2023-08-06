import getopt
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "source:include:omit:", ['source=', 'include=', 'omit='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    command = ['='.join([opt, arg]) for opt, arg in opts]
    os.system('coverage run {} -m unittest discover'.format(' '.join(command)))
    os.system('coverage report -m')
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
