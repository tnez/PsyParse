from psyparse.handler.base_handler import BaseHandler

class DevNull(BaseHandler):
    """The devnull handler provides a mechanism for doing *nothing* with each
    record. This is useful for things like checking for variable names. In this
    case we want to parse the entire logfile, but do nothing with each entry.
    """

    def new(self, entry):
        pass
    
    def update(self, entry, attribute, new_value):
        pass
    