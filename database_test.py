# Test Program for Portfolio Project #

from portfolio import db, Comment
from comments import comments

def add_comment(comment):
    """add a comment to the database, ensure conflicting ids are resolved"""
    # remove pre-existing comment, if the comment_id found in database
    if Comment.query.get(comment.comment_id) is not None:
        db.session.delete(Comment.query.get(comment.comment_id))
    db.session.add(comment)
    db.session.commit()

def test_database():
    """test database functionality"""
    # test that adding, retrieving info works
    add_comment(Comment(12345, "victor", "vge2@illinois.edu", "Hello!",
                        "Wed Oct 29 17:05:33 2014", 0))

    # retrieve the newly stored comment, then verify contents
    retrieved_c = Comment.query.get(12345)
    assert (retrieved_c.comment_id == 12345)
    assert (retrieved_c.name == "victor")
    assert (retrieved_c.email == "vge2@illinois.edu")
    assert (retrieved_c.text == "Hello!")
    assert (retrieved_c.date == "Wed Oct 29 17:05:33 2014")
    assert (retrieved_c.parent_id == 0)

    # add nested responses to first comment
    add_comment(Comment(12346, "victor", "vge2@illinois.edu", "Hello again!",
                        "Wed Oct 29 17:05:34 2014", 12345))
    add_comment(Comment(12347, "victor", "vge2@illinois.edu", "Hello everybody!",
                        "Wed Oct 29 17:05:35 2014", 12346))
    add_comment(Comment(12348, "victor", "vge2@illinois.edu", "Hello to you!",
                        "Wed Oct 29 17:05:36 2014", 12345))
    add_comment(Comment(12349, "victor", "vge2@illinois.edu", "Hello at last!",
                        "Wed Oct 29 17:05:36 2014", 12347))
    add_comment(Comment(12350, "victor", "vge2@illinois.edu", "Hello there!",
                        "Wed Oct 29 17:05:37 2014", 0))

    # test that the structure of the retrieved comments is as expected
    cmts = comments()
    all_cmts = cmts.load(Comment.query.all())

    # test top level comments
    all_ids = [cmt.comment_id for cmt in all_cmts]
    assert (12345 in all_ids and 12350 in all_ids)

    nested_cmts = [cmt for cmt in all_cmts if cmt.comment_id == 12345][0].children

    # test responses to first comment
    nested_ids = [cmt.comment_id for cmt in nested_cmts]
    assert (12346 in nested_ids and 12348 in nested_ids)

    third_cmts = [cmt for cmt in nested_cmts if cmt.comment_id == 12346][0].children

    # test response to the second nested comment
    third_ids = [cmt.comment_id for cmt in third_cmts]
    assert (12347 in third_ids)

    # should be able to go down a few more levels of comments
    last_cmts = third_cmts[0].children[0].children

    # the last comment should have the given id
    assert (len(last_cmts) == 0)

    # remove all of the comments
    db.session.delete(Comment.query.get(12345))
    db.session.delete(Comment.query.get(12346))
    db.session.delete(Comment.query.get(12347))
    db.session.delete(Comment.query.get(12348))
    db.session.delete(Comment.query.get(12349))
    db.session.delete(Comment.query.get(12350))
    db.session.commit()

    print("Database tests passed")

if __name__ == "__main__":
    test_database()

    print("All tests passed")
    
# security notes:
# SQLAlchemy guards against SQL injection attacks, by escaping all values
# unless raw SQL expressions are used, which they aren't in this code
# http://stackoverflow.com/questions/6501583/sqlalchemy-sql-injection
# Jinja2 automatically guards against XSS attacks, by escaping all values
# as long as attributes w/ Jinja expressions are quoted, which the html docs do
# http://flask.pocoo.org/docs/0.10/security/
