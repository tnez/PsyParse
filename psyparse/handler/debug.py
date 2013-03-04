from psyparse.handler.base_handler import BaseHandler

class Debug(BaseHandler):
    """
    The debug handler simply prints the entry object to standard
    output, nothing more.
    """

    def new(self, entry):
        print entry
        
    def update(self, entry, attribute, new_value):
        print "Updating Entry: %s -- %s <-- %s" % (entry.uuid, attribute, new_value)
