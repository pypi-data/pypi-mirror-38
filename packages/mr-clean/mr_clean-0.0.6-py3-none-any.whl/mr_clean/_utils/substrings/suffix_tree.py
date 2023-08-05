# -*- coding: utf-8 -*-
import anytree

# Resources
# https://github.com/cceh/suffix-tree
# https://github.com/Rerito/suffix-tree/blob/master/suffixtree.h
# http://brenden.github.io/ukkonen-animation/

def suffix_tree(str_list):
    # Build suffix tree using Ukkonen’s algorithm
    
    # Return at end
    pass

def suffix_tree_recurse(str_list):
    # Recursively build suffix tree using memoization
    
    # Return at end
    pass


# Maybe extend anytree.Node?


class SNode(anytree.Node):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.end = False
        self.index_dict = None
    
    def add_index(self,index):
        if self.end:
            self.index_dict[index]=True
        else:
            self.index_dict = {index:True}
            self.end = True
    
    def remove_index(self,index):
        try:
            if self.index_dict[index]:
                self.index_dict[index] = False
                return
        except:
            pass
        print("index wasn't in node's index list, couldn't perform remove_index of {}".format(index))
    
    # String index stored as child node whose value is of type int
    # Index Child node only exists when end == True