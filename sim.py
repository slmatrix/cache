#!/usr/bin/python3

import os
import sys
import math

from cache  import cache_set
from parser import get_data

def main(argv):
    #default cache configuration - in bits
    n_way     = int(math.log(0x10    , 0x2));                             #16-way
    line_sz   = int(math.log(0x40    , 0x2));                                #64B
    #cache_sz = int(math.log(0x400, 0x2));                                   #1KB
    #cache_sz = int(math.log(0x8000, 0x2));                                 #32KB
    #cache_sz = int(math.log(0x40000, 0x2));                               #256KB
    cache_sz  = int(math.log(0x100000, 0x2));                                #1MB
    #cache_sz = int(math.log(0x400000, 0x2));                                #4MB
    user_policy = "LRU";

    if len(argv) > 2:                #change defaults to user supplied arguements
      line_sz = int(math.log(int(argv[2]), 2));

      if argv[3] == "1KB":
      	cache_sz = int(math.log(0x400, 0x2));
      elif argv[3] == "32KB":
      	cache_sz = int(math.log(0x8000, 0x2));
      elif argv[3] == "256KB":
      	cache_sz = int(math.log(0x40000, 0x2));
      elif argv[3] == "1MB":
      	cache_sz = int(math.log(0x100000, 0x2));
      elif argv[3] == "4MB":
      	cache_sz = int(math.log(0x400000, 0x2));

      n_way = int(math.log(int(argv[4]), 0x2));
      user_policy = argv[5];

    print(line_sz, cache_sz, n_way, user_policy);
    miss   = 0
    access = 0
    cache  = []
    for i in range((2**(cache_sz - line_sz - n_way))):
        cache.append(cache_set(user_policy, 2**n_way))

    for pc, md, va in get_data(argv[1]):
        offset = va & ((1 << line_sz) - 1);       #only offset bits are unmasked
        va     = va >> line_sz;                              #remove offset bits
        index  = va & ((1 << (cache_sz - line_sz - n_way)) - 1);      #set index
        va     = va >> (cache_sz - line_sz - n_way);          #remove index bits
        tag    = va;                                       #only tag bits remain
        
        if cache[index].search(tag) == False:
            miss += 1;

        access += 1;

    # print("Miss     : ", miss);
    # print("Access   : ", access);
    print("Cache miss rate: ", round((miss/access)*100, 2), "%");


if __name__ == "__main__":
    main(sys.argv);
