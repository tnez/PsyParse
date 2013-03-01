class Logfile(object):

    def __init__(self, filename=None):
        self._filename = filename
        self._mapped_variables = None
        self._unmapped_variables = []
        self._trial_stack = []

    @property
    def trial_stack(self):
        """Return the current trial stack. The hierarchy is represented such
        that the greater the index, the more descendant the trial. The
        zero-indexed element will always represent the current root trial.
        """
        return self._trial_stack


    @property
    def filename(self):
        try:
            return self._filename
        except:
            return None

    @property
    def mapped_variables(self):
        return self._mapped_variables

    @mapped_variables.setter
    def mapped_variables(self, new_map):
        self._mapped_variables = new_map

    @property
    def unmapped_variables(self):
        return self._unmapped_variables

    def register_current_trial(self, new_current_trial):
        """Add a trial to the trial stack. This will determine (using the rep
        and index members) and reorganize the structure of the trial stack on
        the fly.
        """
        

    ## FILE METHODS ###########################################################
    def close(self):
        self._logfile.close()
        self._logfile = None

    def open(self):
        self._logfile = open(self.filename, 'rb')

    def parse(self, handler=None):
        # if no handler has been provided, use the default, debug
        # handler
        if handler is None:
            from .handler.debug import Debug
            handler = Debug()
        # initialize our state variables
        self._current_trial = None
        self._unmapped_variables = []
        try:
            # open the logfile for reading
            self.open()
            line_number = 0
            # for each line in the log file, create a log entry object
            while 1:
                line = self.readline()  # get the next line
                if not line:            # if no line found, EOF, exit
                    break
                # if line is not blank, process line
                line_number += 1
                if len(line) != '\n':
                    current_pos = self.tell()
                    import psyparse.entry
                    entry = psyparse.entry.read(logfile=self, pos=current_pos, raw_entry=line)
                    # handle the entry if it exists
                    if entry is not None:  
                        handler.handle(entry)
                    self.seek(current_pos)  # reset log file position (this
                                            # may have been changed during
                                            # parsing)
            
            # warn the user if any unmapped variables were found
            if len(self.unmapped_variables) > 0:
                import warnings
                print "\n\n"
                warnings.warn("The following variables were found but not mapped: %s"
                              % self.unmapped_variables)
        except Exception as e:
            print "Error in %s: %s (%s)" % (self.filename, line_number, e)
        finally:
            self.close()

    def read(self, num_bytes):
        return self._logfile.read(num_bytes)

    def readline(self):
        line = self._logfile.readline()
        if line == '\n':
            return line
        else:
            return line.strip('\n')

    def seek(self, new_pos):
        self._logfile.seek(new_pos)

    def tell(self):
        return self._logfile.tell()
