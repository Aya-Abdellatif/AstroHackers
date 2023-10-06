from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from util import *
import sqlite3


con = sqlite3.connect("project.sqlite", check_same_thread=False)
cur = con.cursor()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """No Cache"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    return render_template("index.html", log=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'GET':

        if session.get('user_id'):
            return redirect('/')
        else:
            return render_template("login.html")
    else:
        f = request.form

        if None in [f.get('username'), f.get('password')] or '' in [f.get('username'), f.get('password')]:
            return error_message("User does not exist or password is invalid")
        
        student = cur.execute("SELECT * FROM Student WHERE ID = ?", (f.get("username"),))
        s_res = student.fetchall().copy()
        teacher = cur.execute("SELECT * FROM Teacher WHERE ID = ?", (f.get("username"),))
        t_res = teacher.fetchall().copy()
        type = "Teacher"
        if not s_res and not t_res:
            return error_message("User does not exist or password is invalid")
        elif s_res:
            type = "Student"


        password = cur.execute(f'SELECT password FROM {type} WHERE ID = ?', (f.get("username"),))
        password = password.fetchone()[0]
        print(password)
        print(f.get("password"))
        if f.get("password") != password:
            return error_message("User does not exist or password is invalid")

        
        session["user_id"] = f.get("username")
        return redirect('/')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect('/')
        return render_template("registration.html")
    else:
        f = request.form

        if None in [f.get(attribute) for attribute in ["username", "password", "age", "inlineRadioOptions", "type", "name"]] or '' in [f.get(attribute) for attribute in ["username", "password", "age", "inlineRadioOptions", "type", "name"]]:
            ...#return error_message()
        
        student = cur.execute('SELECT age FROM Student WHERE age = ?', (f.get("username"),))
        s_res = student.fetchall().copy()
        teacher = cur.execute('SELECT ID FROM Teacher WHERE ID = ?', (f.get("username"),))
        t_res = teacher.fetchall().copy()

        if s_res or t_res:
            return error_message('User already exists with this username :(')

        type = "Teacher" if f.get("type") == "option2" else "Student"
        gender = "Male" if f.get("inlineRadioOptions") == "option2" else "Female"
        if type == "Teacher":
            cur.execute('INSERT INTO Teacher(ID, password, age, name, gender) VALUES(?, ?, ?, ?, ?)', (f.get("username"), f.get("password"), f.get("age"), f.get("name"), gender))
        else:
            cur.execute('INSERT INTO Student(ID, password, age, name, gender) VALUES(?, ?, ?, ?, ?)', (f.get("username"), f.get("password"), f.get("age"), f.get("name"), gender))
        con.commit()
        session["user_id"] = f.get("username")
        return redirect('/')
    
@app.route('/teachers_info', methods=['GET', 'POST'])
def teachers_info():
    if request.method == "GET":
        return render_template("teachers_info.html")
    else:
        username = request.form.get("username")

        # SQL Qyery to fetch Student IDs
        tbl = []
        query = cur.execute("SELECT ID, name, age, gender FROM Student WHERE teacher_id = ?", (username,)).fetchall()
        for row in query:
            tbl_row = {
                "ID": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3]
            }
            tbl.append(tbl_row)

       

        return render_template("teachers_info.html", tbl=tbl)


