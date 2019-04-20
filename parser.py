"""
  @brief  : parse.py handles reading in cache sequence
  @author : zhongxiu yang
"""

import sys


def main():
    # fetch the path and name to a memory trace file
    gen = get_data(sys.argv[1])
    # print(gen.__next__())


def get_data(filename):
    with open(filename) as f:
        for line in f:
            tokens = line.split()
            if len(tokens) == 3:
                yield int(tokens[0][-2], 16), tokens[1], int(tokens[2], 16)
            else:
                print("Invalid value received")


if __name__ == '__main__':
    main()
