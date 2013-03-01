import psyparse

# create logfile
TEST_LOG_FILE = '/home/tnesland/workspace/psyparse/test_data/katie_2013_Feb_15_1136.log'
logfile = psyparse.Logfile(TEST_LOG_FILE)
print logfile.filename

# map variables
varmap = psyparse.VarMap()
varmap.add('text', 'probe.1', 'Probe')
varmap.add('text_2', 'probe.2', 'Probe')
varmap.add('image', 'image', 'Image')
logfile.mapped_variables = varmap

# parse logfile
logfile.parse()

