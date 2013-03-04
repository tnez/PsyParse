from psyparse.entry import Entry

class Trial(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        self._rep, self._index = _get_rep_and_index(self.log_text)
        logfile.register_current_trial(self)
        self._parent = _get_parent_from_trial_stack(logfile.trial_stack)

    def __str__(self):
        return "Trial: %s Rep: %i Idx: %i Start: %0.4f Stop: %0.4f Parent: %s" \
                % (self.uuid, self.rep, self.index, self.start, self.stop, self.parent)
        
    @property
    def start(self):
        return self.timestamp

    @property
    def stop(self):
        try:
            return self._stop
        except:
            return float('NaN')

    @property
    def index(self):
        return self._index

    @property
    def rep(self):
        return self._rep

    @property
    def parent(self):
        return self._parent
    
    def as_dict(self):
        ret = Entry.as_dict(self)
        ret['start'] = self.start
        ret['stop'] = self.stop
        ret['idx'] = self.index
        ret['rep'] = self.rep
        ret['parent'] = self.parent
        return ret

def read(logfile=None, pos=None, raw_entry=None):
    return Trial(logfile, pos, raw_entry)


def _get_parent_from_trial_stack(trial_stack):
    if len(trial_stack) > 1:
        return trial_stack[-2].uuid
    else:
        return None

def _get_rep_and_index(text):
    import re
    rep = int(re.search('rep=(\d+)', text).group(1))
    index = int(re.search('index=(\d+)', text).group(1))
    return (rep+1, index+1)
