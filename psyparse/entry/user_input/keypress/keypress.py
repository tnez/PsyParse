from psyparse.entry.user_input import UserInput

class Keypress(UserInput):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        UserInput.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        import re
        self._character = re.search('Keypress: (.+)$', raw_entry).group(1)

    def __str__(self):
        return "<Keypress> Char: %s Time: %s Parent: %s" % \
            (self.character, self.timestamp, self.parent)

    @property
    def character(self):
        try:
            return self._character
        except:
            return None
        
    def as_dict(self):
        ret = UserInput.as_dict(self)
        ret['character'] = self.character
        return ret

def read(logfile=None, pos=None, raw_entry=None):
    return Keypress(logfile, pos, raw_entry)
