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
            try:
                pc, md, va = line.split()
                pc = pc[:-1]
                yield int(pc), md, int(va)
            except ValueError:
                print("Invalid value received")


if __name__ == '__main__':
    main()
