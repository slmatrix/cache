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


class cache_set:
    def __init__(self, r_policy, n_way):
        self.n_way    = n_way;
        self.r_policy = r_policy;
        self.tags     = dict();

        #create and initialize the first cache line object in the set
        self.blocks = dummy = node(None, None, None);
        self.evict  = self.blocks.next;

    def search(self, tag):
        if tag in self.tags:                               #is line in the cache
            return True;
        else:                                                 #need to make room
            self.replace(tag);
            return False;

    def replace(self, tag):
        if self.r_policy   == "LRU":
            if len(self.tags) <= self.n_way:   #does set have unallocated slots?
                if self.blocks.next == None:               #allocate first block
                    self.blocks.next = node(line(1, 0, tag), self.blocks, None);
                    self.tags[tag]   = self.blocks.next;
                    self.evict       = self.blocks.next;
                else:                                      #allocate more blocks
                    self.blocks.next = node(line(1, 0, tag), self.blocks,
                                                             self.blocks.next);
                    self.tags[tag] = self.blocks.next;
                    self.blocks.next.next.prev = self.blocks.next;
            elif tag in self.tags:  #update location to head to prevent eviction
                if self.tags[tag] == self.evict:      #update LRU'd block locale
                    self.evict = self.tags[tag].prev;

                self.tags[tag].prev.next = self.tags[tag].next;
                self.tags[tag].prev      = self.blocks;
                self.tags[tag].next      = self.blocks.next;
                self.blocks.next         = self.tags[tag];
            else:        #REPLACEMENT POLICY - overwrite LRU slot with new block
                temp = self.evict.prev;
                print("xxxxx", self.evict.data)
                print(self.evict.data.tag)
                self.tags.pop(self.evict.data.tag);  #remove the LRU'd block tag

                self.evict.data = tag;                #overwrite the LRU'd block
                self.evict.prev = self.blocks;
                self.evict.next = self.blocks.next;

                self.blocks.next.prev = self.evict;   #place at from 'cuz access
                self.blocks.next      = self.evict;
                self.tags[tag]        = self.blocks.next;
                
                self.evict      = temp;           #update point to new LRU block
                self.evict.next = None;
        elif self.r_policy == "SC":
            pass;

        elif self.r_policy == "FIFO":
            pass;


"""
struct fl_entry
{                                      /* frames represented by a linked list */
  uint64_t frame_number;         /* O(n) lookup of frame number, O(1) updates */
  uint64_t* pt_entry;         /* unset old valid-bit & assign new page->frame */
  struct fl_entry* next;              /* order of frames represent LRU policy */
};

void update_fl(struct fl_entry* frames,
               uint64_t         frame_number)
{
  struct fl_entry* dummy = frames->next;
  while(true)
  {
    if(frames->next->frame_number == frame_number)        /* most recent page */
    {                                                       /* accessed again */
      return ;
    }
    else if(dummy->next->frame_number == frame_number)
    {                           /* update page access, relative to frame list */
      struct fl_entry* swap = dummy->next;
      dummy->next = dummy->next->next;
      swap->next = frames->next;
      frames->next = swap;
      break;
    }
    else
    {
      dummy = dummy->next;
    }
  }
}

void handle_page_fault(struct fl_entry* frames,
                       uint64_t*        page_table,
                       uint64_t         page_number)
{
  static uint64_t frames_allocated = 0;      //first page is allocated to kernel
  struct fl_entry* dummy = frames->next;
  while(true)
  {
    if(frames->next->frame_number == UNALLOCATED)     /* base-case: no memory */
    {                                                        /* allocated yet */
      frames_allocated += 1;
      frames->next->frame_number = frames_allocated;
      frames->next->pt_entry = page_table+page_number; /* reverse mapping PTE */
      page_table[page_number] = frames->next->frame_number;
      break;
    }
    else if(dummy->frame_number != UNALLOCATED &&        /* found unallocated */
            dummy->next->frame_number == UNALLOCATED)      /* frame in memory */
    {
      struct fl_entry* swap = dummy->next;                     /* empty frame */
      dummy->next = dummy->next->next;           /* remove from orig position */
      swap->next = frames->next;          /* and place at head; recent access */
      frames->next = swap;

      frames_allocated += 1;
      swap->frame_number = frames_allocated;
      swap->pt_entry = page_table+page_number;     /* new reverse mapping PTE */
      page_table[page_number] = swap->frame_number;
      break;
    }
    else if(dummy->next->next == NULL)                    /* PAGE REPLACEMENT */
    {
      struct fl_entry* swap = dummy->next;          /* evict frame; overwrite */
      dummy->next = NULL;                         /* dummy is now at end; LRU */
      swap->next = frames->next;                    /* place new page at head */
      frames->next = swap;

      *(swap->pt_entry) = DISK;                         /* invalidate old PTE */
      swap->pt_entry = page_table+page_number;     /* new reverse mapping PTE */
      page_table[page_number] = swap->frame_number;             /* update PTE */
      break;
    }
    else
    {
      dummy = dummy->next;
    }
  }
}
"""
