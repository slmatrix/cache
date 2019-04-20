class node:
    def __init__(self, line, next):
        self.data = data;
        self.next = next;


class linked_list:
    def __init__(self, head):
        self.head = head;


class set:
    def __init__(self, r_policy, n_way):
        self.n_way    = n_way;
        self.r_policy = r_policy;

        self.tags = dict();
        self.blocks = dummy = linked_list(None, None);
        for line in range(0, n_way):
            dummy.next = node(line(0, 0, 0), None);
            dummy = dummy.next;

    def search(self, tag):
        if tag in self.tags:                               #is line in the cache
            return True;
        else:                                                 #need to make room 
            replace(tag);
            return False;

    def replace(self, tag):
        if self.r_policy   == "LRU":
            pass;
        elif self.r_policy == "SC":
            pass;
        elif self.r_policy == "FIFO":
            pass;


class line:
    def __init__(self, valid, dirty, tag):
        self.tag   = tag;
        self.valid = valid;
        self.dirty = dirty;
        self.data  = [None] * 0x40
