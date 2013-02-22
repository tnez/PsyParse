from ..entry import Entry

class Trial(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        self._end = self._get_end_time(logfile)
        self._uuid = self._generate_uuid()
        self._index = self._get_trial_index()

    def __str__(self):
        return "<TRIAL> UUID: %s Idx: %i Start: %0.4f End: %0.4f" % \
            (self.uuid, self.index, self.start, self.end)
        
    @property
    def start(self):
        return self.timestamp

    @property
    def end(self):
        try:
            return self._end
        except:
            return None

    @property
    def index(self):
        try:
            return self._index
        except:
            return None

    @property
    def uuid(self):
        try:
            return self._uuid
        except:
            return None

    def _generate_uuid(self):
        import uuid
        return uuid.uuid4()

    def _get_end_time(self, logfile):
        # there is no end trial log, so we need to scan forward for
        # the next new trial or EOF
        line = None
        while 1:
            last_line = line                # store last line
            line = logfile.readline().strip('\n') # get new line
            # if we have reached the end of the file we need to get
            # the timestamp from the last known line
            if not line:
                return float(last_line.split('\t')[0])
            if "New trial" in line:
                return float(line.split('\t')[0])

    def _get_trial_index(self):
        import re
        text = self.log_text
        rep = int(re.search('rep=(\d+)', text).group(1))
        index = int(re.search('index=(\d+)', text).group(1))
        return (index + 1) * (rep + 1)
        

def read(logfile=None, pos=None, raw_entry=None):
    return Trial(logfile, pos, raw_entry)

