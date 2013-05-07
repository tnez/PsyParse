class BaseHandler(object):
    """
    An abstract hanlder class to help define how a handler should behave. No
    methods are actually implemented and will raise a not-implemented error
    if an instance of a handler subclass does not implement any of the 
    following methods.
    """
    def new(self, entry):
        """Create a new entry"""
        raise Exception("""'new' method not defined in handler subclass""")
        
    def update(self, entry, attribute, new_value):
        """Update a given entry. This is useful when properties of a given
        entry are only discovered sometime later in parsing."""
        raise Exception("""'update' method not defined in handler subclass""")
