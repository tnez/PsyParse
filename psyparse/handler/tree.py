from psyparse.handler.pydict import PyDict

class Tree(PyDict):
    """Logfile handler that is capable of writing to csv file after parsing."""
    def __init__(self):
        PyDict.__init__(self)
        self._map = None
        self._tree = None
    
    def children(self, uuid):
        """Return children of an event (specified by UUID) as a tree with 
        specified event as the root all descendants."""
        result = {k:v for k,v in self.data.items()
                  if v.get('parent', None) == uuid}
        for uuid,record in result.items():
            children = self.children(uuid)
            if len(children) > 0:
                record['children'] = children
            else:
                continue
        return result
    
    def find_nearest_node(self, uuid, field, value):
        """Return the node nearest to the specified node where the specified 
        field contains the specified value. This method starts at the sibling 
        level and traverses up the tree, thus no nodes descending from the 
        specified node will be searched."""
        # we might be the nearest node... so first check ourself for match
        record = self.data[uuid]
        found = record.get(field, None)
        if found == value:
            return record
        # next check siblings
        for _,record in self.siblings(uuid).items():
            # if the we find the expected value for the given field in the
            # record, return the entire record
            found = record.get(field, None)
            if found == value:
                return record
        # value was not found in siblings, so search whilst traversing up the 
        # tree, starting at the parent, which is one level up
        uuid = self.data[uuid].get('parent', None)
        level = 1
        while uuid is not None:
            record = self.data[uuid]
            found = record.get(field, None)
            # if the expected value for the given field was found, return the
            # entire record
            if found == value:
                return record
            # if we are at least 2 levels up from original node, we must also
            # check the children of the current node (I guess these are cousin
            # nodes?)
            if level >= 2:
                for _,record in self.children(uuid).items():
                    found = record.get(field, None)
                    if found == value:
                        return record
            # since nothing yet has been found, continue up the tree
            uuid = self.data[uuid].get('parent', None)
            level += 1
        # no acceptable value was found, so return None
        return None
    
    def siblings(self, uuid):
        """Return siblings of a node (specified by UUID). If no siblings were
         found, or if none could be found due to existing tree structure, 
         return None. Note: the parent of the given node is used to 
         determine siblings, thus if the given node has no parent, no siblings
         will be returned regardless of perceived structure."""
        parent_uuid = self.data[uuid].get('parent', None)
        if parent_uuid is None:
            return {}
        else:
            # get all children of the parent of the given node
            siblings = {k:v for k,v in self.data.items()
                        if v.get('parent', None) == parent_uuid}
            # remove the given node, for it is not a sibling of itself
            del siblings[uuid]
            return siblings
        
    def tree_map(self):
        if self._tree_map is not None:
            return self._tree_map
        else:
            self._group_by_root()
            return self._tree_map

    def tree(self):
        if self._tree is not None:
            return self._tree
        else:
            self._group_by_root()
            return self._tree
        
    def write(self, filename, root_event):
        pass        

    def _group_by_root(self):
        # return groups of roots as a tree, and a map of each uuid to its
        # location in the tree
        tree = {k:v for k,v in self.data.items() if v['parent'] is None}
        for uuid, record in tree.items():
            record['children'] = self.children(uuid)
        self._tree = tree
        self._tree_map = self._treeMap(self._tree)
        
    def _treeMap(self, tree):
        tree_map = dict()
        def map_entries(tree_map, key_path=[]):
            for uuid, record in tree_map.items():
                tree_map[uuid] = key_path + [uuid]
                children = record.get('children', None)
                if children is not None:
                    map_entries(children, key_path + [uuid,'children'])
        return tree_map
        
