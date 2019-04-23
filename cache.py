from collections import OrderedDict;


class node:
    def __init__(self, data, prev, next):
        self.data = data;
        self.prev = prev;
        self.next = next;


class line:
    def __init__(self, valid, dirty, tag):
        self.tag   = tag;
        self.valid = valid;
        self.dirty = dirty;
        self.data  = [None] * 0x40

        self.second_chance = 1;             #used only for SC replacement policy


class cache_set:
    def __init__(self, r_policy, n_way):
        self.n_way    = n_way;
        self.r_policy = r_policy;
        self.tags     = OrderedDict();

        #create and initialize the first cache line object in the set
        #self.blocks = node(None, None, None); #head pointer (most recently used)
        #self.evict  = self.blocks.next;      #tail pointer (leastly recent used)

    def search(self, tag):
        if tag in self.tags:    #need to update existing block's eviction notice
            self.replace(tag);
            return True;
        else:                                           #need write in new block
            self.replace(tag);
            return False;

    def replace(self, tag):
        if self.r_policy == "LRU":
            if tag in self.tags:             #new access; update locale in queue
                block          = self.tags.pop(tag);
                self.tags[tag] = block;
#                if len(self.tags) == 1:  #edge case: only one blk, no reordering
#                    return ;
#
#                temp = self.evict;
#                if self.tags[tag] == self.evict:      #update LRU'd block locale
#                    temp = self.evict.prev;
#
#                self.tags[tag].prev.next = self.tags[tag].next;
#                self.tags[tag].prev      = self.blocks;
#                self.tags[tag].next      = self.blocks.next;
#
#                self.blocks.next.prev    = self.tags[tag];
#                self.blocks.next         = self.tags[tag];
#
#                self.evict      = temp; #edge case: in-case LRU'd was referenced
            elif len(self.tags) < self.n_way:    #set not full; create new entry
                self.tags[tag] = line(1, 0, tag);

#                if self.blocks.next == None:               #allocate first block
#                    self.blocks.next = node(line(1, 0, tag), self.blocks, None);
#                    self.tags[tag]   = self.blocks.next;
#                    self.evict       = self.blocks.next;
#                else:                                      #allocate more blocks
#                    self.blocks.next = node(line(1, 0, tag), self.blocks,
#                                                             self.blocks.next);
#                    self.tags[tag] = self.blocks.next;
#                    self.blocks.next.next.prev = self.blocks.next;
            else:        #REPLACEMENT POLICY - overwrite LRU slot with new block
                self.tags.popitem(last=False);
                self.tags[tag] = line(1, 0, tag);

                
#                temp = self.evict.prev;
#                self.tags.pop(self.evict.data.tag);  #remove the LRU'd block tag
#
#                self.evict.data.tag = tag;            #overwrite the LRU'd block
#                self.evict.prev     = self.blocks;
#                self.evict.next     = self.blocks.next;
#
#                self.blocks.next.prev = self.evict;   #place at from 'cuz access
#                self.blocks.next      = self.evict;
#                self.tags[tag]        = self.evict;
#                
#                self.evict      = temp;           #update point to new LRU block
#                self.evict.next = None;


        elif self.r_policy == "SC":
            pass;


        elif self.r_policy == "FIFO":
            pass;
