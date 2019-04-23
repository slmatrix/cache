"""
  @brief  : parse.py handles reading in cache sequence
  @author : zhongxiu yang
"""

import sys

def get_data(filename):
    with open(filename) as f:
        for line in f:
            tokens = line.split()
            if len(tokens) == 3:
                yield int(tokens[0][-2], 16), tokens[1], int(tokens[2], 16)
            else:
                pass
