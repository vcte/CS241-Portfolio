# Test Program for Portfolio Project #

from database_test import test_database
from svn_test import test_log_get_info, test_lst_get_info
from utility_test import test_utility_all

def all_tests():
    """run all tests, for all units"""
    test_database()
    test_log_get_info()
    test_lst_get_info()
    test_utility_all()

if __name__ == "__main__":
    all_tests()

    print("All tests passed")
    
