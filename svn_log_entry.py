# SVN log entry class #

class svn_log_entry:
    """class to represent a log entry in the svn log"""
    def __init__(self, rev, auth, date, msg):
        """constructor - set all values of the object"""
        self.rev  = rev
        self.auth = auth
        self.date = date
        self.msg  = msg
        self.paths = []
    def add_path(self, path, kind, act):
        """method to add a new path to list of paths
           each path represented as a dictionary storing information"""
        self.paths.append( { 'path' : path, 'kind' : kind, 'act' : act } )

    def get_paths(self):
        """getter method, to get the list of paths"""
        return self.paths
