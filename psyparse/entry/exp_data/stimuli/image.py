from psyparse.entry.exp_data.stimuli.base_stimulus import BaseStimulus

class Image(BaseStimulus):
    
    def __init__(self, logfile=None, pos=None, raw_entry=None,
                 orig_var_name=None, trans_var_name=None):
        BaseStimulus.__init__(self, logfile, pos, raw_entry, orig_var_name,
                              trans_var_name)
        self.filename = get_filename(logfile, orig_var_name)

    def __str__(self):
        return "Image: %s Filename: %s Start: %s End: %s Parent: %s" % \
            (self.uuid, self.filename, self.start, self.stop, self.parent)
            
    @property
    def filename(self):
        try:
            return self._filename
        except:
            return None
        
    @filename.setter
    def filename(self, new_filename):
        self._filename = new_filename
        
    def as_dict(self):
        ret = BaseStimulus.as_dict(self)
        ret['filename'] = self.filename
        return ret
    
def get_filename(logfile, var_name):
    # read backwards until we find "Set %orig_name image="
    search_string = "Set %s image=" % var_name
    search_string_len = len(search_string)
    next_pos = logfile.tell()
    while 1:
        pos = next_pos
        logfile.seek(pos)
        text = logfile.read(search_string_len)
        if text == search_string:
            try:
                text = logfile.readline()
                import os.path
                return os.path.basename(text)
            except:
                return None 
        if pos < 0:
            return None # we've gone through the whole file and not
                        # found what we were looking for
        else:
            next_pos = pos - 1
            
def read(logfile=None, pos=None, raw_entry=None,
         orig_var_name=None, trans_var_name=None):
    return Image(logfile, pos, raw_entry, orig_var_name, trans_var_name)