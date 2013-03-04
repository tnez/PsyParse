from psyparse.entry import Entry

class UserInput(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)
        self.parent = logfile.trial_stack[-1].uuid
        
    @property
    def parent(self):
        try:
            return self._parent
        except:
            return None
        
    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent
        
    def as_dict(self):
        ret = Entry.as_dict(self)
        ret['parent'] = self.parent
        return ret

################################################################################
def read(logfile=None, pos=None, raw_entry=None):
    _,_,text = raw_entry.split('\t') # get relavent text entry
    if "Keypress: " in text:
        import keypress
        return keypress.read(logfile, pos, raw_entry)
    else:
        print Entry(logfile, pos, raw_entry)
