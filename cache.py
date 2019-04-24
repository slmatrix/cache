from collections import OrderedDict;

class line:
    def __init__(self, valid, dirty, tag, second_chance=True):
        self.tag   = tag;
        self.valid = valid;
        self.dirty = dirty;
        self.data  = [None] * 0x40
        self.second_chance = second_chance; #used only for SC replacement policy


class cache_set:
    def __init__(self, r_policy, n_way):
        self.n_way    = n_way;
        self.r_policy = r_policy;
        self.tags     = OrderedDict();

    def search(self, tag):
        if tag in self.tags:    #need to update existing block's eviction notice
            self.replace(tag);
            return True;
        else:                                           #need write in new block
            self.replace(tag);
            return False;

    def replace(self, tag):
        if self.r_policy == "LRU":
            if tag in self.tags:     #new access; update locale in queue to head
                block          = self.tags.pop(tag);
                self.tags[tag] = block;
            elif len(self.tags) < self.n_way:    #set not full; create new entry
                self.tags[tag] = line(1, 0, tag);
            else:        #REPLACEMENT POLICY - overwrite LRU slot with new block
                self.tags.popitem(last=False);   #overwrite oldest accessed line
                self.tags[tag] = line(1, 0, tag);

        elif self.r_policy == "SC":
            if tag in self.tags:                     #new access; set chance bit
                self.tags[tag].second_chance = True;
            elif len(self.tags) < self.n_way:    #set not full; create new entry
                self.tags[tag] = line(1, 0, tag);
            else:  #REPLACEMENT POLICY - overwrite oldest slot when not accessed
                for i in range(len(self.tags)+1):
                    block = self.tags.popitem(last=False);
                    block = block[1];
                    if block.second_chance == False:
                        self.tags[tag] = line(1, 0, tag);
                        return ;
                    else:
                        self.tags[block.tag] = line(1, 0, block.tag, False);

        elif self.r_policy == "FIFO":
            if tag in self.tags:
                return ;                              #do nothing in case of hit
            elif len(self.tags) < self.n_way:    #set not full; create new entry
                self.tags[tag] = line(1, 0, tag);
            else:                    #REPLACEMENT POLICY - overwrite oldest slot
                self.tags.popitem(last=False);            #overwrite oldest line
                self.tags[tag] = line(1, 0, tag);

        elif self.r_policy == "LIFO":
            if tag in self.tags:
                return ;                              #do nothing in case of hit
            elif len(self.tags) < self.n_way:    #set not full; create new entry
                self.tags[tag] = line(1, 0, tag);
            else:                    #REPLACEMENT POLICY - overwrite newest slot
                self.tags.popitem(last=True);             #overwrite newest line
                self.tags[tag] = line(1, 0, tag);
