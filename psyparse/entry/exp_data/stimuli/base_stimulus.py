from ...entry import Entry
from ....varmap import VarMap

class BaseStimulus(Entry):

    def __init__(self, logfile=None, pos=None, raw_entry=None,
                 orig_var_name=None, trans_var_name=None):
        Entry.__init__(self, logfile, pos, raw_entry)
        self._orig_name = orig_var_name
        self._name = trans_var_name
        self._start = float(raw_entry.split('\t')[0])
        self._end = get_end_time(logfile, orig_var_name)

        @property
        def name(self):
            try:
                return self._name
            except:
                return None

        @property
        def start(self):
            try:
                return self._start
            except:
                return None

        @property
        def end(self):
            try:
                return self._end
            except:
                return None
        

def get_end_time(logfile, var_name):
    # read forward until we find 'Stopped presenting
    # %orig_var_name' or EOF
    line = None
    while 1:
        last_line = line # store the last read line
        line = logfile.readline()
        # if we have reached EOF, take timestamp from last
        # line
        if not line:
            return float(last_line.split('\t')[0])
        if "Stopped presenting %s" % var_name in line:
            return float(last_line.split('\t')[0])

def read(logfile=None, pos=None, raw_entry=None):
    var_name = raw_entry.split()[-1]
    mapped_var = logfile.mapped_variables.get(var_name, None)
    if mapped_var is not None:
        mapped_klass = __import__(mapped_var.klass, globals(), locals(), ['read'], -1)
        return mapped_klass.read(logfile, pos, raw_entry, var_name, mapped_var.transformed_name)
    else:
        if var_name not in logfile.unmapped_variables:
            logfile.unmapped_variables.append(var_name)
        return None
