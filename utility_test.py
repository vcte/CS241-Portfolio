# Test Program for Portfolio Project #

from utility import find_type, clean_date, pick_color, filter_words

def test_find_type():
    """test find_type function"""
    # test that correct types are returned for given file extensions
    assert (find_type("chess.java") == "code")
    assert (find_type("program.rb") == "code")
    assert (find_type("pic.png") == "img")
    assert (find_type("board.jpg") == "img")
    assert (find_type("animation.gif") == "img")
    assert (find_type("data.db") == "data")
    assert (find_type("data.xml") == "data")
    assert (find_type("hubs.json") == "data")
    assert (find_type("test_plan.pdf") == "doc")
    assert (find_type("document.docx") == "doc")

    # test that default value is given for unregonized extensions
    assert (find_type("none.none") == None)
    assert (find_type("folder") or "dir" == "dir")
    assert (find_type("file.ext") or "file" == "file")

    print("find_type test passed")

def test_clean_date():
    """test clean_date function"""
    # test that svn date strings can be cleaned properly
    assert (clean_date("2014-09-25T22:41:51.353") == "2014-09-25 @ 22:41:51")
    assert (clean_date("2014-09-25T22:41:51")     == "2014-09-25 @ 22:41:51")
    assert (clean_date("2014-09-25 @ 22:41:51.353") == "2014-09-25 @ 22:41:51")

    print("clean_date test passed")

def test_pick_color():
    # test border cases
    assert (pick_color(1) == "#C0A76F")
    assert (pick_color(25) == "#A9EE17")

    # test invalid indexes
    assert (pick_color(0) == "#000000")
    assert (pick_color(-1) == "#000000")
    assert (pick_color(26) == "#000000")

    print("pick_color test passed")

def test_filter_words():
    # test innocuous cases
    assert (filter_words("Hello world!") == "Hello world!")
    assert (filter_words("ABC 123 $%^") == "ABC 123 $%^")

    # test that subset of flagged words are filtered
    assert (filter_words("the ARSE, said DAGO") == "the ***** said ****")
    assert (filter_words("a SPAZ did WOG") == "a **** did ***")

    # test that non-alphabetical characters can be handled
    assert (filter_words("SPIC!, goes the [JIGAB] TWAT.")
            == "****** goes the ******* *****")
    assert (filter_words("SHT SH!T SH!!T SH!i!T")
            == "*** **** ***** ******")
    assert (filter_words("WEED-COK/HOOKER+KIKE") == "**** *** ****** ****")

    # test that upper and lower cases are handled
    assert (filter_words("DYKE dyke Dyke DyKe") == "**** **** **** ****")

    print("filter_words test passed")
    
def test_utility_all():
    """run all tests for utility module"""
    test_find_type()
    test_clean_date()
    test_pick_color()
    test_filter_words()
    
    print("utility tests passed")

if __name__ == "__main__":
    test_utility_all()

    print("All tests passed")
    
