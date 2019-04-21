class node:
    def __init__(self, data, next):
        self.data = data;
        self.next = next;


class line:
    def __init__(self, valid, dirty, tag):
        self.tag   = tag;
        self.valid = valid;
        self.dirty = dirty;
        self.data  = [None] * 0x40


class cache_set:
    def __init__(self, r_policy, n_way):
        self.n_way    = n_way;
        self.r_policy = r_policy;
        self.tags     = dict();

        #create and initialize the cache lines in the set
        self.blocks = dummy = node(None, None);
        for i in range(0, n_way):
            dummy.next = node(line(0, 0, 0), None);
            dummy = dummy.next;

    def search(self, tag):
        if tag in self.tags:                               #is line in the cache
            return True;
        else:                                                 #need to make room
            self.replace(tag);
            return False;

    def replace(self, tag):
        if self.r_policy   == "LRU":
            if len(self.tags) <= self.n_way:
                self.tags[tag] = self.blocks.next;

        elif self.r_policy == "SC":
            pass;

        elif self.r_policy == "FIFO":
            pass;
