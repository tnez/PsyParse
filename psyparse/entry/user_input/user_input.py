from ..entry import Entry

class UserInput(Entry):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None):
        Entry.__init__(self, logfile=logfile, pos=pos, raw_entry=raw_entry)

################################################################################
def read(logfile=None, pos=None, raw_entry=None):
    _,_,text = raw_entry.split('\t') # get relavent text entry
    if "Keypress: " in text:
        import keypress
        return keypress.read(logfile, pos, raw_entry)
    else:
        print Entry(logfile, pos, raw_entry)
