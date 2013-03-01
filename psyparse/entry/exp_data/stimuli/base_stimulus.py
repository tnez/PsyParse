from psyparse.entry import Entry

class BaseStimulus(Entry):

    def __init__(self,logfile=None, pos=None, raw_entry=None,
                 orig_var_name=None, trans_var_name=None):
        
        Entry.__init__(self, logfile, pos, raw_entry)
        self._orig_name = orig_var_name
        self.name = trans_var_name
        self.start = self.timestamp
        self.stop = get_stop_time(logfile, orig_var_name)

        @property
        def name(self):
            try:
                return self._name
            except:
                return None
            
        @name.setter
        def name(self, new_name):
            self._name = new_name

        @property
        def start(self):
            try:
                return self._start
            except:
                return None
            
        @start.setter
        def start(self, new_start):
            self._start = new_start

        @property
        def stop(self):
            try:
                return self._end
            except:
                return None

        @stop.setter
        def stop(self, new_stop):
            self._stop = new_stop


def get_stop_time(logfile, var_name):
    # read forward until we find 'Stopped presenting
    # %orig_var_name' or EOF
    line = None
    search_string = 'Stopped presenting %s' % var_name
    while 1:
        last_line = line # store the last read line
        line = logfile.readline()
        # if we have reached EOF, take timestamp from last
        # line
        if not line:
            return float(last_line.split('\t')[0])
        if line[-len(search_string):] == search_string:
            return float(line.split('\t')[0])

def read(logfile=None, pos=None, raw_entry=None):
    var_name = raw_entry.split()[-1]
    mapped_var = logfile.mapped_variables.get(var_name, None)
    if mapped_var is not None:
        mapped_klass = __import__(mapped_var.klass, globals(), locals(),
                                  ['read'], -1)
        return mapped_klass.read(logfile, pos, raw_entry, var_name,
                                 mapped_var.transformed_name)
    else:
        if var_name not in logfile.unmapped_variables:
            logfile.unmapped_variables.append(var_name)
        return None
