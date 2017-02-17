# Portfolio Project #
# url - https://victor-portfolio-cs242.herokuapp.com/

# import flask libraries
from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

# import general libraries
from lxml import objectify
import os
import time

# import local code
from svn_log import svn_log
from svn_list import svn_list
from comments import comments
from utility import filter_words

# set up flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] \
                                        if 'DATABASE_URL' in os.environ \
                                        else "postgres://ubqyguuwrmmtte:udJU9xiZTJEVQYQfexckCNzGPC@ec2-54-225-156-230.compute-1.amazonaws.com:5432/d9c23q4e3qt33u"
db = SQLAlchemy(app)

# set up database model
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80))
    email      = db.Column(db.String(120))
    text       = db.Column(db.Text)
    date       = db.Column(db.String(40))
    parent_id  = db.Column(db.Integer)

    # constructor function
    def __init__(self, comment_id, name, email, text, date, parent_id):
        self.comment_id = comment_id
        self.name       = name
        self.email      = email
        self.text       = text
        self.date       = date
        self.parent_id  = parent_id

    # string conversion function
    def __repr__(self):
        return "<Comment %i, by %s, at %s>" % \
               (self.comment_id, self.name, self.date)

# default url
@app.route("/")
def main():
    return "Hello World! <br>" + \
           "<a href=\"portfolio/\">See portfolio</a>"

# url to view portfolio
@app.route("/portfolio/")
def portfolio():
    """return static portfolio main page"""
    return render_template("portfolio.html")

# url to view specific project in portfolio
@app.route("/portfolio/<project_name>", methods=['GET'])
def portfolio_project(project_name = None):
    """create page from template, use information about given project"""
    # render project page, use default value of 0 (root) for parent comment_id
    return render_project(project_name)

# url to view specific project, and reply to a specific comment
@app.route("/portfolio/<project_name>", methods=['POST'])
def portfolio_project_reply(project_name = None):
    """create project page from template, pass info about comment parent"""
    # pass along comment_id of parent comment, so reply can store parent_id
    par_comment = request.form['comment_id']
    return render_project(project_name, par_comment)

def render_project(project_name = None, par_comment = 0):
    """helper function for portfolio_project and portfolio_project_reply"""
    return render_template("portfolio_project.html",
                           project_info = get_project_info(project_name),
                           comments = load_comments(),
                           par_comment = par_comment)

# url to view specific file in project
@app.route("/view/<file_type>/<path:file_path>")
def portfolio_view(file_type = None, file_path = None):
    """create page from template, use the given file path as input to iframe"""
    return render_template("portfolio_view.html",
                           file_type = file_type,
                           file_path = file_path)

# url to post new comment - comments shared across both projects
@app.route("/portfolio/<project_name>/comment", methods=['POST'])
def portfolio_comment(project_name = None):
    # retrieve all inputted values
    name  = request.form['name'] or ""
    email = request.form['email'] or ""
    text  = request.form['comment'] or ""
    par   = request.form['parent_id'] or ""
    text = filter_words(text)

    # route the user to a different page, depending on whether input is valid
    if not(len(name) < 1 or len(name) > 80 or len(email) > 120):
        add_comment(name, email, text, par)
        return render_template("portfolio_comment.html",
                               project_name = project_name)
    else:
        return render_template("portfolio_error.html",
                               project_name = project_name)

def get_project_info(project_name):
    """get information for given project, return as a dictionary"""
    # load svn log data and svn list data
    (log_data, lst_data) = load_svn_data()
    
    # initialize dict, which contains info for the project
    project_info = {}
    
    # if project_name is given as url, then only take last part of url
    if '/' in project_name:
        project_name = project_name[project_name.find('/') + 1 :]

    # mapping from website's name for project, and official name
    name_to_assignment = { "Chess" : "Assignment 1",
                           "CSAir" : "Assignment 2" }

    # get official assignment name, error if not correct name
    if not project_name in name_to_assignment:
        return {}
    else:
        assignment_name = name_to_assignment[project_name]
    
    # set title info
    project_info['title'] = project_name

    # get most recent date, version, commit summary for the project
    (date, vers, summ) = log_data.get_project_info(assignment_name)
    project_info['date'] = date
    project_info['vers'] = vers
    project_info['summ'] = summ

    # get listing of all files in project
    files = lst_data.get_project_info(assignment_name)
    project_info['files'] = files

    return project_info

def add_comment(name, email, text, par):
    """add a new comment to the database, with unique comment_id"""
    # next comment id is one greater than the current highest comment id
    next_id = max([cmt.comment_id for cmt in Comment.query.all()]) + 1
    new_cmt = Comment(next_id, name, email, text, time.asctime(), par)
    db.session.add(new_cmt)
    db.session.commit()
    
def load_svn_data():
    """load svn log, list data from xml files, parse data,
       return log and list data, as data encapsulated in class"""
    # process svn log file
    log_file = open('svn_log.xml', 'r')
    log_str  = "".join(log_file.readlines())
    log_xml  = objectify.fromstring(log_str)
    log_data = svn_log(log_xml)
    log_file.close()

    # process svn list file
    lst_file = open('svn_list.xml', 'r')
    lst_str  = "".join(lst_file.readlines())
    lst_xml  = objectify.fromstring(lst_str)
    lst_data = svn_list(lst_xml)
    lst_file.close()

    return (log_data, lst_data)

def load_comments():
    """load comment data from database, return as Python object"""
    # comments class takes care of parsing all objects in database
    cmts = comments()
    cmts.load(Comment.query.all())
    return cmts.getComments()

if __name__ == "__main__":
    """main function - run web app"""
    app.run()
