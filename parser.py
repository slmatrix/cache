"""
  @brief  : parse.py handles reading in cache sequence
  @author : zhongxiu yang
"""


def get_data(infile):
    pass

def main():
    # fetch the path and name to a memory trace file
    cache_file = open(sys.argv[1], "r")
    # fetch the size and way of the cache
    # cache_size = sys.argv[2]
    # cache_way = sys.argv[3]
    caches = []
    for lines in cache_file:
        line = lines.split()
        line[0] = line[0][:-1]
        t = tuple(line)
        caches.append(t)
        # set associative
        # replacement: LRU policy (either use a queue or an extra field in the cache frame to record the access time stamp to each cache line)
        # write: write-back policy
    cache_file.close()


if __name__ == '__main__':
    main()
