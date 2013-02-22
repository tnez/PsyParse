from ..entry import Entry

def read(logfile=None, pos=None, raw_entry=None):
    _,_,text = raw_entry.split('\t') # get relavent text entry
    for phrase in _ignore_list():
        if phrase in text:
            return None
    if "New trial" in text:
        import trial
        new_trial = trial.read(logfile, pos, raw_entry)
        logfile.current_trial = new_trial
        return new_trial
    if "Started presenting" in text:
        import stimuli
        return stimuli.read(logfile, pos, raw_entry)
    else:
        print "This event is not handled: %s" % Entry(logfile, pos, raw_entry)

def _ignore_list():
    return [
        "Imported ",
        "Created sequence: ",
        "Stopped presenting",
        "Set "
        ]
