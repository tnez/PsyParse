class Mapping(object):
    
    def __init__(self, map_tuple):
        if map_tuple:
            self._klass = map_tuple[1]
            self._transformed_name = map_tuple[0]
        else:
            self = None

    @property
    def klass(self):
        try:
            return self._klass
        except:
            return None

    @property
    def transformed_name(self):
        try:
            return self._transformed_name
        except:
            return None

class VarMap(dict):

    def add(self, orig_name, new_name, klass_name):
        """Add an entry to the variable map. This will map the
        orig_name (name as it appears in the logfile) to a given class
        and name each instance by the given new name.
        """
        if klass_name in available_classes():
            klass_path = _class_hash()[klass_name]
            self[orig_name] = Mapping((new_name, klass_path))
        else:
            raise Exception("%s is not in list of available classes" % klass_name)
    
    def klass(self, orig_name):
        try:
            return self[orig_name].klass
        except:
            return None

    def transformed_name(self, orig_name):
        try:
            return self[orig_name].transformed_name
        except:
            return None

def read_varmap(varmap):
    """
    Given a plain text variable file in the following format:

    orig_name     new_name     var_klass
    image         image        image
    text          probe.1      probe
    text_2        probe.2      probe

    Each variable will be associated with a class (determined by
    case-insensitive match against all filenames sitting at or below
    entry module.

    When the parser encounters the given variable name in text, it
    will create an instance of the mapped class and will set its name
    attribute equal to the new var name.
    """
    new_varmap = VarMap()
    try:
        f = open(varmap, 'rb')
        for line in f.readlines():
            orig_name, new_name, klass = line.split()
            new_varmap[orig_name] = Mapping((new_name, klass))
    except Exception as e:
        print e
    finally:
        f.close()
    return new_varmap

def available_classes():
    """
    List all available valid classes that can be used for mapping
    variables.
    """
    ret = []
    for mapping in _read_available_classes():
        ret.append(mapping['name'])
    return ret

def attributes_for_class(klass_name):
    if klass_name not in available_classes():
        print "%s is not registered as an available class" % klass_name
    # create an empty varmap to use within this function
    varmap = VarMap()
    # add our specified class to the varmap using dummy variable names
    # (only the class is important)
    varmap.add('foo', 'foo', klass_name)
    # import our specified klass
    klass_file = __import__(varmap['foo'].klass, fromlist=[klass_name])
    klass = getattr(klass_file, klass_name)
    # inspect our class instance
    # 1) get every member for our given class and put it in a list
    # 2) for every item in that list, print to console
    import inspect
    members = [x[0] for x in inspect.getmembers(klass) if not x[0].startswith('_')]
    print "\nAccessible attributes for %s are as follows:\n" % klass_name
    for member in members:
        print "\t%s" % member

def _read_available_classes():
    import os.path
    libdir = '%s/../lib' % (os.path.abspath(os.path.dirname(__file__)))
    f = open('%s/klass_map.txt' % libdir, 'rb')
    try:
        while 1:
            line = f.readline()
            if not line:
                break
            if line[0] == '#':
                continue
            if (line) != '\n':
                name, path = line.strip('\n').split()
                yield {'name': name, 'path': path}
    except Exception as e:
        print "There was a problem with the class map: %s" % e
    finally:
        f.close()

def _class_hash():
    ret = {}
    for entry in _read_available_classes():
        ret[entry['name']] = entry['path']
    return ret
