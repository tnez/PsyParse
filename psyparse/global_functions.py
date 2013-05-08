# Module level functions

def sample_log_file():
    """Return the path to a sample logfile as a convenience for the
    user to have some sample data to play with and get a feel for this
    code."""
    import os.path
    psyparse_home = os.path.abspath(os.path.dirname(__file__))
    tests_dir = os.path.join(psyparse_home, 'tests')
    test_data_dir = os.path.join(tests_dir,'data')
    SAMPLE_FILE_OF_CHOICE = 'SUB002_2013_Feb_15_1231.log'
    return test_data_dir + '/' + SAMPLE_FILE_OF_CHOICE
