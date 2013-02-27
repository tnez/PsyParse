from .base_stimulus import BaseStimulus

class Probe(BaseStimulus):

    def __init__(self, logfile=None, pos=None, raw_entry=None,
                 orig_var_name=None, trans_var_name=None):
        BaseStimulus.__init__(self, logfile, pos, raw_entry, orig_var_name,
                              trans_var_name)
        self._position = get_position(logfile, orig_var_name)

    def __str__(self):
        return "<Probe> X: %0.1f Y: %0.1f Start: %s End: %s" % \
            (self.x, self.y, self.start, self.end)

    @property
    def position(self):
        """Return location in pixels"""
        try:
            return self._position
        except:
            return None

    @property
    def x(self):
        try:
            return self.position[0]
        except:
            return None

    def y(self):
        try:
            return self.position[1]
        except:
            return None

def get_position(logfile, var_name):
    # read backwards until we find "Set %orig_name pos="
    search_string = "Set %s pos=" % var_name
    search_string_len = len(search_string)
    pos = logfile.tell()
    while 1:
        text = logfile.read(search_string_len)
        if text == search_string:
            import re
            match = re.search('\[ *(\d*\.d*) +(\d*\.d*) *\]', text)
            return (float(match.group(1)), float(match.group(2)))
        pos -= 1 + search_string_len
        if pos < 0:
            return None # we've gone through the whole file and not
                        # found what we were looking for
        else:
            logfile.seek(pos)

def read(logfile=None, pos=None, raw_entry=None,
         orig_var_name=None, trans_var_name=None):
    return Probe(logfile, pos, raw_entry, orig_var_name, trans_var_name)
