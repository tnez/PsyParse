from psyparse.handler.tree import Tree

class Frame(Tree):
    """A data frame that maps data relating to the given nodes.
    
        nodes - a list of 2-tuples in the form of (field,value) that specifies
                for which nodes data should be queried. Example: 
                [('name','image')]specifies that for every node where the name
                field is equivalent to 'image', variables will be mapped.
                
        variables - a list of 3-tuples in the form of (field,value,var_field)
                    that specifies both a mapping to a neighboring node
                    (specified by field and value in the same manner as the
                     node argument) and the field for which the value should
                    be extracted. Example: [('class','trial','duration')]
                    specifies that for all nodes, the nearest neighboring node
                    where the field class is equivalent to 'trial' will be
                    asked the value that resides in the 'duration' field.
                    
        header - a list of strings representing the header of the data frame;
                 order should correspond to variables
    """
    def __init__(self, nodes=[], variables=[], header=[], sort_by=[]):
        Tree.__init__(self)
        self._is_dirty = True
        self.nodes = nodes
        self.variables = variables 
        self.header = header
        self._values = None
        self._selected_nodes = None
        self._sort_by = sort_by
        
    def __str__(self):
        if self.header is not None:
            print self.header
        print self.values

    def head(self, number_of_records=10):
        """Print the first few records."""
        # print the header
        print ','.join(map(str,self.header)) # print the header
        # print the first few records
        records = self.values
        for i in range(0, number_of_records):
            try:
                print ','.join(map(str, records[i]))
            except IndexError:
                break
                
    @property
    def nodes(self):
        return self._nodes
    
    @nodes.setter
    def nodes(self, new_nodes):
        self._nodes = new_nodes
        self._build_selected_nodes()
        self._is_dirty = True
        
    @property
    def selected_nodes(self):
        if self._selected_nodes is None:
            self._build_selected_nodes()
        return self._selected_nodes
    
    @property
    def sort_by(self):
        return self._sort_by
    
    @sort_by.setter
    def sort_by(self, new_sort_by):
        # make sure all elements are in header
        for item in new_sort_by:
            if item not in self.header:
                raise Exception("%s was not found in header -- sort_by was not set" % new_sort_by)
        # go ahead and sort elements
        else:
            self._sort_by = new_sort_by

    @property
    def values(self):
        # rebuild values if changes have been made since last build
        if self._is_dirty:
            self._build_selected_nodes()
            self._build_values()
        # if we have a list of sort by keys, loop through in reverse
        # order, sorting by each key, so that the end result is sorted
        # by keys, in the order specified
        if len(self.sort_by) >= 1:
            tmp_values = self._values
            for sort_key in reversed(self.sort_by):
                sort_index = self.header.index(sort_key)
                tmp_values = sorted(tmp_values, key=lambda record: record[sort_index])
            return tmp_values
        else:
            return self._values
    
    @property
    def variables(self):
        return self._variables
    
    @variables.setter
    def variables(self, new_variables):
        self._variables = new_variables
        self._is_dirty = True

    def write_to_csv(self, filename):
        import csv
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(self.header)
            for record in self.values:
                writer.writerow(record)
    
    def _build_values(self):
        # reset values
        self._values = []
        # for all selected nodes
        for uuid in self.selected_nodes:
            record = []
            for field,value,var_field in self.variables:
                nearest_node = self.find_nearest_node(uuid, field, value)
                if nearest_node is not None:
                    value = nearest_node.get(var_field, None)
                else:
                    value = None
                record.append(value)
            self._values.append(record)
        self._is_dirty = False
            
    def _build_selected_nodes(self):
        self._selected_nodes = []
        for field,value in self.nodes:
            found_nodes = {k:v for k,v in self.data.items()
                           if v.get(field, None) == value}
            self._selected_nodes += found_nodes.keys()
         
         
    
