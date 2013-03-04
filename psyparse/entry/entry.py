class Entry(object):

    def __init__(self, logfile=None, pos=None, raw_entry=None):
        self.timestamp, self.log_type, self.log_text = raw_entry.split('\t')
        self._uuid = _generate_uuid()
        
    def __str__(self):
        return "%0.4f\t%s\t%s" % (self.timestamp, self.log_type, self.log_text)

    @property
    def log_text(self):
        try:
            return self._log_text
        except:
            return None

    @log_text.setter
    def log_text(self, _text):
        self._log_text = _text

    @property
    def log_type(self):
        try:
            return self._log_type
        except:
            return None

    @log_type.setter
    def log_type(self, _type):
        self._log_type = _type

    @property
    def name(self):
        try:
            return self._name
        except:
            return self.__class__.__name__
        
    @name.setter
    def name(self, new_name):
        self._name = new_name 
    
    @property
    def timestamp(self):
        try:
            return self._timestamp
        except:
            return None

    @timestamp.setter
    def timestamp(self, _timestamp):
        self._timestamp = float(_timestamp)
        
    @property
    def uuid(self):
        return self._uuid
    
    def as_dict(self):
        return {
                'log_text': self.log_text,
                'timestamp': self.timestamp
                }
    
# MODULE LEVEL FUNCTIONS
def read(logfile=None, pos=None, raw_entry=None):
    # send entry on to propper parser based on type
    _,log_type,_ = raw_entry.split('\t')
    if log_type == 'DATA':
        import user_input
        return user_input.read(logfile, pos, raw_entry)
    elif log_type == 'EXP':
        import exp_data
        return exp_data.read(logfile, pos, raw_entry)
    elif log_type == 'DEBUG':
        pass
    elif log_type == 'INFO':
        pass
    else:
        print "I do not handle the following entry: %s" % Entry(logfile,pos,raw_entry)
        
def _generate_uuid():
    import uuid
    return uuid.uuid4()
