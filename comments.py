# Comments class #

# import statements
from comment import comment

class comments:
    """class to represent / store list of top-level comments"""
    def __init__(self):
        self.comments = []

    def load(self, db_comment_list):
        """load, organize comment data from list of all comments in database"""
        # create temporary 'root' comment, w/ unique comment_id of 0
        root = comment(0, "", "", "")

        # recursively add children of root, starting w/ top level comments
        self.addChildren(root, db_comment_list)

        # retrieve children of root, which are all top level comments
        self.comments = root.children

        # sort by id in ascending order, so that oldest comments appear first
        self.comments = sorted(self.comments, key = lambda x: x.comment_id)
        return self.comments

    def addChildren(self, parent, db_comment_list):
        """recursively add children of parent comment"""
        # search through all comments retrieved from the database
        for db_comment in db_comment_list:
            # look for comments whose parent is the current comment
            if parent.comment_id == db_comment.parent_id:
                # construct Python object for comment, and add to parent
                cmt = comment(db_comment.comment_id, db_comment.name,
                              db_comment.text, db_comment.date)
                #print("adding " + str(cmt) + " to " + str(parent))
                parent.addChild(cmt)
                self.addChildren(cmt, db_comment_list)

    def getComments(self):
        """getter function to retrieve list of top-level comments"""
        return self.comments
