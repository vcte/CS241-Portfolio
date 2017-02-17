# Test Program for Portfolio Project #

from lxml import objectify

import svn_log
import svn_list
import portfolio

def test_log_get_info():
    """test that get_project_info for svn log retrieves most recent results"""
    (log_data, lst_data) = portfolio.load_svn_data()

    # unrecognized project name should return empty tuple
    assert (log_data.get_project_info("ABC")
            == ())

    # passing in name for 'Chess' project should return most recent info
    assert (log_data.get_project_info("Assignment 1")
            == ('2014-09-25 @ 22:41:51', '4997',
                'added GUI interactivity, move highlighting, ' +
                'forfeit / restart, undo / redo, pawn promotion'))

    # passing in name for 'CSAir' project should return most recent info
    assert (log_data.get_project_info("Assignment 2")
            == ('2014-10-16 @ 22:57:20', '7288', 'assignment 2.2'))

def test_lst_get_info():
    """test that get_project_info for svn list retrieves files in directory"""
    (log_data, lst_data) = portfolio.load_svn_data()

    # unrecognized project name should return empty list
    assert (lst_data.get_project_info("ABC")
            == [])

    # test that certain files are contained in list of files for chess project
    files_1 = lst_data.get_project_info("Assignment 1")
    files_1 = map(lambda file: file.path, files_1)
    assert ("Assignment 1.2" in files_1)
    assert ("Assignment 1.2/Chess.iml" in files_1)
    assert ("Assignment 1.2/src/Chess/Movement/Movements.java" in files_1)
    assert ("Assignment 1.2/src/Chess/Pieces/Monkey.java" in files_1)
    assert ("Assignment 1.2/src/Chess/Resources/Icons/Black/bq.png" in files_1)
    assert ("Assignment 1.2/src/Test/BoardTest.java" in files_1)

    # test that certain files are contained in list of files for cs air project
    files_2 = lst_data.get_project_info("Assignment 2")
    files_2 = map(lambda file: file.path, files_2)
    assert ("Assignment 2.2" in files_2)
    assert ("Assignment 2.2/.idea/CSAir.iml" in files_2)
    assert ("Assignment 2.2/res/cmi_hub.json" in files_2)
    assert ("Assignment 2.2/src/Test/cmd_spec.rb" in files_2)
    assert ("Assignment 2.2/src/graph.rb" in files_2)
    assert ("Assignment 2.2/test_plan.pdf" in files_2)

if __name__ == "__main__":
    test_log_get_info()
    test_lst_get_info()

    print("All tests passed")
    
