from psyparse.handler.base_handler import BaseHandler

class PyDict(BaseHandler):
    """Logfile handler that holds objects as nested python dictionaries"""
    
    def __init__(self):
        BaseHandler.__init__(self)
        self.data = dict()
        self.mappings = []
        
    def new(self, entry):
        self.mappings = [entry.uuid, entry.name]
        if not self.data.has_key(entry.name):
            self.data[entry.name] = dict()
        self.data[entry.name][entry.uuid] = entry.as_dict()
        
    def update(self, entry, attribute, new_value):
        """Update the entry so that attribute is set to new value"""
        self.data[entry.name][entry.uuid][attribute] = new_value
        
def _get_name_for_uuid(mappings, target_uuid):
    """Return the name for the given uuid or return None if not found.""" 
    for uuid, name in mappings:
        if uuid == target_uuid:
            return name
    return None
            