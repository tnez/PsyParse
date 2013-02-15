class Logfile(object):
    
    def __init__(self, filename=None, db_obj=None):
        if filename is not None:
            self.filename = filename
        if db_obj is not None:
            self.db_obj = db_obj

    @property
    def filename(self):
        try:
            return self._filename
        except:
            return None

    @property
    def db_obj(self):
        try:
            return self._db_obj
        except:
            return None

    def parse():
        f = open(filename, 'rb')
        lines = f.readlines() # for now this is fine, but eventually
                              # this should be changed so that the
                              # logfile is not read all at once, maybe
                              # just pass a reference to the logfile
                              # and pointer to the object rather than
                              # the lines object

        # create an object capable of mapping lines to event types
        mapper = Mapper()
        for line in lines:
            mapper.map(line)
        
