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
    
    def klass(self, orig_name):
        try:
            return self[orig_name].klass
        except:
            return None

    def transformed_name(self, orig_name):
        try:
            return self[orig_name].klass
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
    import inspect, sys.modules
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        print name
        
