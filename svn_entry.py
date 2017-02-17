# SVN entry class #

class svn_entry:
    """class to represent an entry in the svn list"""
    def __init__(self, kind, type, path, name, size, rev, auth, date):
        # all attributes passed in should be strings
        self.kind = kind
        self.type = type
        self.name = name
        self.path = path
        self.size = size
        self.rev  = rev
        self.auth = auth
        self.date = date
