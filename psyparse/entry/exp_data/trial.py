from ..entry import Entry

class Trial(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        self._stop = _get_stop_time(logfile)
        self._uuid = _generate_uuid()
        self._rep, self._index = _get_rep_and_index(self.log_text)
        logfile.register_current_trial(self)
        self._parent = self._get_parent_from_trial_stack(logfile.trial_stack)

    def __str__(self):
        return "<Trial> Rep: %i Idx: %i Start: %0.4f Stop: %0.4f Parent: %s" \
                % (self.rep, self.index, self.start, self.stop, self.parent)
        
    @property
    def start(self):
        return self.timestamp

    @property
    def stop(self):
        try:
            return self._stop
        except:
            return None

    @property
    def index(self):
        return self._index

    @property
    def rep(self):
        return self._rep
    
    @property
    def uuid(self):
        try:
            return self._uuid
        except:
            return None



def read(logfile=None, pos=None, raw_entry=None):
    return Trial(logfile, pos, raw_entry)

def _generate_uuid(self):
    import uuid
    return uuid.uuid4()

def _get_parent_from_trial_stack(trial_stack):
    if len(trial_stack) > 1:
        return trial_stack[-2].parent
    else:
        return None

def _get_rep_and_index(text):
    import re
    rep = int(re.search('rep=(\d+)', text).group(1))
    index = int(re.search('index=(\d+)', text).group(1))
    return (rep+1, index+1)
    
def _get_stop_time(logfile):
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
        


