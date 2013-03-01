from ...entry import Entry


class Keypress(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        import re
        self._character = re.search('Keypress: (.+)$', raw_entry).group(1)
        self._trial_id = logfile.current_trial.uuid

    def __str__(self):
        return "<Keypress> Char: %s Time: %s Trial_ID: %s" % \
            (self.character, self.timestamp, self.trial_id)

    @property
    def character(self):
        try:
            return self._character
        except:
            return None

    @property
    def trial_id(self):
        try:
            return self._trial_id
        except:
            return None
    
def read(logfile=None, pos=None, raw_entry=None):
    return Keypress(logfile, pos, raw_entry)
