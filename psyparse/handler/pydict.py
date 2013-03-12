from psyparse.handler.base_handler import BaseHandler

class PyDict(BaseHandler):
    """Logfile handler that holds objects as nested python dictionaries"""
    
    def __init__(self):
        BaseHandler.__init__(self)
        self.data = dict()        
        
    def new(self, entry):
        self.data[entry.uuid] = entry.as_dict()
        
    def update(self, entry, attribute, new_value):
        """Update the entry so that attribute is set to new value"""
        self.data[entry.uuid][attribute] = new_value