#!/usr/bin/python3

import os
import sys
import math

from cache  import cache_set
from parser import get_data

def main(argv):
    #default cache configuration - in bits
    n_way    = int(math.log(0x10    , 0x2));                             #16-way
    line_sz  = int(math.log(0x40    , 0x2));                                #64B
    cache_sz = int(math.log(0x100000, 0x2));                                #1MB

    if len(argv) > 2:               #change defaults to user supplied arguements
        pass
    else:
        pass

    miss   = 0
    access = 0
    cache  = []
    for i in range((2**(cache_sz - line_sz - n_way))):
        cache.append(cache_set("LRU", 2**n_way))

    for pc, md, va in get_data(argv[1]):
        offset = va & ((1 << line_sz) - 1);       #only offset bits are unmasked
        va     = va >> line_sz;                              #remove offset bits
        index  = va & ((1 << (cache_sz - line_sz - n_way)) - 1);      #set index
        va     = va >> (cache_sz - line_sz - n_way);          #remove index bits
        tag    = va;                                       #only tag bits remain
        
        if cache[index].search(tag) == False:
            miss += 1;

        access += 1;

    print("Miss  : ", miss);
    print("Access: ", access);
    print("Miss ratio: ", miss/access);


if __name__ == "__main__":
    main(sys.argv);
