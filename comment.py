# Comment class #

# import statements
import re
from utility import pick_color

class comment:
    """class to represent a single comment"""
    def __init__(self, comment_id, name, text, date):
        """default constructor - set all values of object"""
        self.comment_id = comment_id
        self.name       = name
        self.text       = text
        self.date       = date
        self.children   = []
        
    def addChild(self, child):
        """add a nested child comment, to children array"""
        self.children.append(child)
        
    def getDate(self):
        """get date info, but w/ unneeded text removed"""
        # extract 'month day', and 'year' text from date, using regex
        return ", ".join(
            re.search(r'\w+\s*(\w+\s*\d+)\s*\d+.\d+.\d+\s*(\d+)', self.date)
            .groups())

    def getHash(self, string):
        """deterministic hash function, transform string into a number"""
        # output is in range: [1 .. 25]
        return (sum([ord(char) * (123456789) for char in string]) % 25) + 1

    def getPic(self):
        """get picture for icon, by hashing the name of the comment's writer"""
        return str(self.getHash(self.name))

    def getColor(self):
        """get corresponding border color for picture, by taking same hash"""
        return pick_color(self.getHash(self.name))
