# SVN list class #

import svn_entry
import utility

class svn_list:
    """class to represent the svn list, contains relevant data"""
    def __init__(self, lst_xml):
        """read svn list data in xml format, convert to python data structures"""
        # find first list, should only find one list
        lst = lst_xml.find("list")
        self.path = lst.attrib['path']
        self.entries = []
        for entry in lst.findall("entry"):
            # values are empty string by default, if no attribute found
            entry_path = entry.find("name").text
            entry_name = entry_path[entry_path.find("/") + 1 :] \
                         if "/" in entry_path else entry_path
            commit_info = entry.find("commit")
            entry_size = entry.find("size") if entry.find("size") else ""
            entry_kind = entry.attrib['kind'] if 'kind' in entry.keys() else ""
            entry_type = utility.find_type(entry_name) or entry_kind
            entry_date = utility.clean_date(commit_info.find("date").text)

            # construct a new entry object, with info, to add to list
            new_entry = svn_entry.svn_entry(
                                  kind = str(entry_kind),
                                  type = entry_type,
                                  name = entry_name,
                                  path = entry_path,
                                  size = str(entry_size),
                                  rev  = commit_info.attrib['revision'],
                                  auth = commit_info.find("author").text,
                                  date = entry_date)
            self.entries.append(new_entry)
    
    def get_project_info(self, assignment_name):
        """get list of all files for a project"""
        # mapping to get most recent version of assignment
        most_recent_assignments = { "Assignment 1" : "Assignment 1.2",
                                    "Assignment 2" : "Assignment 2.2" }

        # try to find most recent version of assignment, same name if not found
        assignment_name = most_recent_assignments.get(assignment_name,
                                                      assignment_name)
        
        # get all files stored in a directory, within the assignment directory
        files = [ entry for entry in self.entries
                  if entry.path.startswith(assignment_name) ]

        return files
