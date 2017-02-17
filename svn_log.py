# SVN log class #

import svn_log_entry
import utility

class svn_log:
    """class to represent the svn log, contains relevant data"""
    def __init__(self, log_xml):
        """read svn log data in xml format, convert to python data structures"""
        # all data is stored in log_entries list
        self.log_entries = []
        for log_entry in log_xml.findall("logentry"):
            # create a new log entry, with given info
            log_date = utility.clean_date(log_entry.find("date").text)
            new_log_entry = svn_log_entry.svn_log_entry(
                                          rev  = log_entry.attrib['revision'],
                                          auth = log_entry.find("author").text,
                                          date = log_date,
                                          msg  = log_entry.find("msg").text)

            # add every directory path, with info, to the log entry object
            for path in log_entry.find("paths").findall("path"):
                # value set to empty string if element does not have attribute
                path_kind = path.attrib['kind'] if 'kind' in path.keys() else ""
                path_act  = path.attrib['action'] if 'action' in path.keys() else ""

                # add new path to log entry's list of paths, using class method
                new_log_entry.add_path(path = path.text,
                                       kind = path_kind,
                                       act  = path_act)
            self.log_entries.append(new_log_entry)
            
    def get_project_info(self, assignment_name):
        """get most recent date, version, commit summary for a project"""
        # get all log entries, which have a file in the given project directory
        entries = [ entry for entry in self.log_entries
                    if any([path['path'].startswith("/vge2/" + assignment_name)
                            for path in entry.get_paths() ]) ]

        # error if no log entries with given project directory
        if len(entries) < 1:
            return ()

        # find most recent revision of the project, by sorting the entries
        entries = sorted(entries, key = lambda entry: int(entry.rev))
        entry  = entries[len(entries) - 1]

        return (entry.date, entry.rev, entry.msg)
