from utils.control import Analyzer
from icecream import ic
import sys

def main():
    analyzer = Analyzer()
    analyzer.read_csv(sys.argv[1])
    ic(analyzer.X, analyzer.Y)


if __name__ == '__main__':
    main()

