from utils.control import Analyzer
import sys

def main():
    analyzer = Analyzer()
    analyzer.read_csv(sys.argv[1])


if __name__ == '__main__':
    main()

