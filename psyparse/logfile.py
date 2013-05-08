class Logfile(object):

    def __init__(self, filename=None):
        self._filename = filename
        self._logfile = None
        from .varmap import VarMap
        self._mapped_variables = VarMap()
        self._unmapped_variables = []
        self._sequence_stack = []
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
    def handler(self):
        try:
            return self._hanlder
        except:
            from .handler.debug import Debug
            self._handler = Debug()
            return self._handler
    
    @handler.setter
    def handler(self, new_handler):
        self._hanlder = new_handler
        
    @property
    def mapped_variables(self):
        return self._mapped_variables

    @mapped_variables.setter
    def mapped_variables(self, new_map):
        self._mapped_variables = new_map

    @property
    def unmapped_variables(self):
        return self._unmapped_variables
    
    def find_unmapped_variables(self):
        """List all the variables found in the given logfile that will require
        mapping."""
        # get the old parser if it exists
        old_handler = self.handler
        from .handler.devnull import DevNull
        self.handler = DevNull()
        self.parse()
        print "" # print a pretty newline
        if len(self._unmapped_variables) > 0:
            print "The following unmapped variables were found:"
            for var in self._unmapped_variables:
                print var
        else:
            print "No unmapped variables were found."
        # return the old parser, just in case the user had preset
        self.handler = old_handler
    
    def parse(self):
        # initialize our state variables
        self._sequence_stack = []
        self._trial_stack = []
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
                if line != '\n':
                    current_pos = self.tell()
                    from . import entry
                    entry = entry.read(logfile=self, pos=current_pos, raw_entry=line)
                    # handle the entry if it exists
                    if entry is not None:  
                        self.handler.new(entry)
                    self.seek(current_pos)  # reset log file position (this
                                            # may have been changed during
                                            # parsing)
            
            # clear out and update all trials remaining in trial stack
            self._unravel_trial_stack()

        except Exception as e:
            print "Error in %s: %s (%s)" % (self.filename, line_number, e)
        finally:
            self.close()    

    def register_current_sequence(self, num_types, num_reps):
        """Add a sequence to the sequence stack. This sequence information is
        used to manage the organization of the trial stack. 
        """
        self._sequence_stack.append({'idx': num_types, 'rep': num_reps})
    
    def register_current_trial(self, new_current_trial):
        """Add a trial to the trial stack. This will determine (using the rep
        and index members) and reorganize the structure of the trial stack on
        the fly.
        """
        # descend the trial stack, and while the most recent trial
        # represents the last trial in a sequence, remove that trial and
        # sequence
        while len(self._sequence_stack) > 0 and len(self._trial_stack) > 0 and \
            self._trial_stack[-1].rep == self._sequence_stack[-1]['rep'] and \
            self._trial_stack[-1].index == self._sequence_stack[-1]['idx']:
            # remove sequence
            self._sequence_stack.pop()
            # remove trial and update stop time
            last_trial = self._trial_stack.pop()
            self.handler.update(last_trial, 'stop', new_current_trial.start)
        # if our sequence stack is deeper than our trial stack, we need to
        # append to our trial stack
        if len(self._sequence_stack) > len(self._trial_stack):
            self._trial_stack.append(new_current_trial)
        else:
            # replace the most recent trial in the stack with our new current
            # trial and update stop time for the trial we are removing
            last_trial = self._trial_stack.pop()
            self.handler.update(last_trial, 'stop', new_current_trial.start)
            self._trial_stack.append(new_current_trial)
    
    def _get_last_time_stamp(self):
        """Get the last time stamp in the logfile. This is needed to resolve
        stop times for final trial branch."""
        self.open()
        try:
            line = None
            while 1:
                line = self.readline()
                if not line:
                    break
                if line != '\n':
                    last_line = line
            timestamp,_,_ = last_line.split('\t')
            return timestamp
        except:
            return float('NaN')
        finally:
            self.close()
        
    def _unravel_trial_stack(self):
        """Unravel trial stack so that end times are recorded for the last
        branch of trials."""
        last_time_stamp = self._get_last_time_stamp()
        while len(self.trial_stack) > 0:
            last_trial = self.trial_stack.pop()
            self.handler.update(last_trial, 'stop', last_time_stamp)

    ## FILE METHODS ###########################################################
    def close(self):
        if self._logfile is not None:
            self._logfile.close()
            self._logfile = None

    def open(self):
        if self._logfile is not None:
            if not self._logfile.closed:
                self._logfile.close()
        self._logfile = open(self.filename, 'rb')            

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
