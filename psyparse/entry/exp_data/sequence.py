from psyparse.entry import Entry

class Sequence(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        self._nTrials, self._nReps = _parse_sequence(raw_entry)
        logfile.register_current_sequence(self._nTrials, self._nReps)
        
def read(logfile=None, pos=None, raw_entry=None):
    return Sequence(logfile, pos, raw_entry)

def _parse_sequence(text):
    import re
    try:
        nTrials = int(re.search('trialTypes=(\d+)', text).group(1))
        nReps = int(re.search('nReps=(\d+)', text).group(1))
        return nTrials, nReps
    except:
        return None
    