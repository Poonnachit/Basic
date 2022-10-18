import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flaskext.mysql import MySQL
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pymysql
import time
import datetime
from function import allowed_file_pdf, allowed_file_py, grading_system, allowed_file_txt
from os.path import exists
import filecmp
import subprocess

app = Flask(__name__)
CORS(app)

app.secret_key = "mysecretkey"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 's64160038'
app.config['MYSQL_DATABASE_PASSWORD'] = 's64160038'
app.config['MYSQL_DATABASE_DB'] = 's64160038'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)


@app.route("/")
def home():
    if "email" in session:

        sql = """
        SELECT * 
        FROM basic_user_ln_lab
        WHERE basic_user_id = %s
        ORDER BY basic_user_ln_lab_created_date
        DESC LIMIT 1;
        """
        cursor.execute(sql, session["id"])
        user_ln_lab = cursor.fetchone()

        
        if user_ln_lab is None:
            lab_id = 2
            sql = """
            SELECT *
            FROM basic_labs
            WHERE basic_lab_id = %s
            """
            cursor.execute(sql, lab_id)
            data = cursor.fetchone()

            lab_name = data["basic_lab_name"]
            lab_description = data["basic_lab_description"]
            lab_url = url_for("lab", lab_id=lab_id)
            user_lab_file = {}
            user_lab_file['basic_user_lab_score'] = 0
            return render_template("index.html", lab_name=lab_name, lab_description=lab_description, lab_url=lab_url,lab_progress=user_lab_file)

        else:
            lab_id = user_ln_lab["basic_lab_id"]
            sql = """
            SELECT *
            FROM basic_labs
            WHERE basic_lab_id = %s
            """
            cursor.execute(sql, lab_id)
            data = cursor.fetchone()

            lab_name = data["basic_lab_name"]
            lab_description = data["basic_lab_description"]
            lab_url = url_for("lab", lab_id=lab_id)
            sql = """
            SELECT * 
            FROM basic_user_lab_file
            WHERE basic_user_ln_lab_id = %s
            ORDER BY basic_user_lab_score
            DESC LIMIT 1;
            """
            cursor.execute(sql, user_ln_lab["basic_user_ln_lab_id"])
            user_lab_file = cursor.fetchone()
            return render_template("index.html", lab_name=lab_name, lab_description=lab_description, lab_url=lab_url, lab_progress=user_lab_file)
    return redirect(url_for("login"))


@app.route("/stage_labs")
def all_labs_stage():
    if "email" in session:
        sql = """\
        SELECT * FROM basic_labs\
        """
        cursor.execute(sql)
        datas = cursor.fetchall()
        # print(datas)
        sql = """
        SELECT DISTINCT basic_lab_id, max(basic_user_lab_score) FROM basic_user_lab_file NATURAL JOIN basic_user_ln_lab NATURAL JOIN basic_labs WHERE basic_user_id = %s GROUP BY basic_lab_id;
        """
        cursor.execute(sql, session["id"])
        user_labs = cursor.fetchall()
        # print(user_labs)
        test_labs = []
        for data in datas:
            for user_lab in user_labs:
                print(user_lab)
                if data["basic_lab_id"] == user_lab["basic_lab_id"]:
                    data["basic_lab_progress"] = user_lab["max(basic_user_lab_score)"]
            test_labs.append(data)
                # else:
                #     data["basic_lab_progress"] = 0
                #     test_labs.append(data)
        print(test_labs)
        return render_template("all_lab_stage.html", datas=test_labs)
    return redirect(url_for("login"))

@app.route("/stage_lessons")
def all_lessons_stage():
    return render_template("all_lesson_stage.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM basic_users WHERE basic_user_email = %s AND basic_user_password = %s",
                       (email, password))
        data = cursor.fetchone()
        if data:
            session['id'] = data['basic_user_id']
            session['first_name'] = data['basic_user_first_name']
            session['last_name'] = data['basic_user_last_name']
            session['email'] = email
            sql = """
            UPDATE basic_users 
            SET basic_user_update_date = NOW() 
            WHERE basic_user_email = %s
            """
            cursor.execute(sql, email)
            conn.commit()
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return render_template('index.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM basic_users WHERE basic_user_email = %s", email)
        data = cursor.fetchone()
        if data:
            flash("Email already exists")

        else:
            sql = """
            INSERT INTO basic_users (basic_user_first_name, basic_user_last_name, basic_user_email, basic_user_password) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (first_name, last_name, email, password))
            conn.commit()
            return redirect(url_for('login'))
    return render_template("register.html")


@app.route('/lesson/<lessonName>')
def lesson(lessonName):
    if "email" in session:
        return render_template(lessonName + ".html")
    return redirect(url_for("login"))


@app.route('/lab/<lab_id>', methods=['GET', 'POST'])
def lab(lab_id):
    if "email" in session:
        sql = """
        SELECT * FROM basic_user_ln_lab WHERE basic_user_id = %s AND basic_lab_id = %s
        """
        cursor.execute(sql, (session['id'], lab_id))
        data_user = cursor.fetchone()
        if data_user:
            sql = """
            UPDATE basic_user_ln_lab
            SET basic_user_ln_lab_update_date = NOW()
            WHERE basic_user_id = %s AND basic_lab_id = %s
            """
            cursor.execute(sql, (session['id'], lab_id))
            conn.commit()

            basic_user_ln_lab_id = data_user["basic_user_ln_lab_id"]
            sql = """
            SELECT * FROM basic_user_lab_file WHERE basic_user_ln_lab_id = %s
            """
            cursor.execute(sql, basic_user_ln_lab_id)
            submission_data = cursor.fetchall()
        else:
            sql = """
            INSERT INTO basic_user_ln_lab (basic_user_id, basic_lab_id)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (session['id'], lab_id))
            conn.commit()
            sql = """
            SELECT * FROM basic_user_ln_lab WHERE basic_user_id = %s AND basic_lab_id = %s
            """
            cursor.execute(sql, (session['id'], lab_id))
            data_user = cursor.fetchone()
            basic_user_ln_lab_id = data_user["basic_user_ln_lab_id"]
            sql = """
            SELECT * FROM basic_user_lab_file WHERE basic_user_ln_lab_id = %s
            """
            cursor.execute(sql, basic_user_ln_lab_id)
            submission_data = cursor.fetchall()

        sql = """
        SELECT * FROM basic_labs WHERE basic_lab_id = %s
        """
        cursor.execute(sql, lab_id)
        data = cursor.fetchone()
        name = data['basic_lab_name']
        desc = data['basic_lab_description']
        filename = data['basic_lab_file_name']

        if request.method == "POST":

            UPLOAD_FOLDER = '/home/BUU/64160038/Basic/uploads/user'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            user_ln_lab_id = request.form['user_ln_lab_id']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file_py(file.filename):
                current_time = time.time()
                filename = str(int(current_time)) + secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                sql = """
                INSERT INTO basic_user_lab_file (basic_user_ln_lab_id, basic_user_lab_file_path)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (user_ln_lab_id, filename))
                conn.commit()
            if not (allowed_file_py(file.filename)):
                flash('Please upload .py file')
                return redirect(request.url)
            file_exists = exists(file_path)
            if file_exists:
                sql = """
                SELECT * FROM basic_lab_testcase WHERE basic_lab_id = %s
                """
                cursor.execute(sql, lab_id)
                data_testcase = cursor.fetchall()
                all_testcase = 0
                passed_testcase = 0
                for testcase in data_testcase:
                    all_testcase += 1
                    # print(grading_system(testcase['basic_input_path'], testcase['basic_output_path'], filename, file_path))
                    if grading_system(testcase['basic_input_path'], testcase['basic_output_path'], filename, file_path):
                        passed_testcase += 1
                sql = """
                UPDATE basic_user_lab_file 
                SET basic_user_lab_score = %s
                WHERE basic_user_ln_lab_id = %s
                AND basic_user_lab_file_path = %s
                """
                # print(filename)
                score = str((passed_testcase / all_testcase) * 100)
                cursor.execute(sql, (score, user_ln_lab_id, filename))
                conn.commit()
                return redirect(url_for('lab', lab_id=lab_id))
            flash("File not found")
            return redirect(request.url)
        return render_template("lab.html", name=name, desc=desc, filename=filename, submission=submission_data,
                               user_ln_lab_id=data_user['basic_user_ln_lab_id'])
    return redirect(url_for("login"))

@app.route('/create_lab', methods=['GET', 'POST'])
def create_lab():
    UPLOAD_FOLDER = '/home/BUU/64160038/Basic/static/labs'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        lab_name = request.form['labname']
        lab_description = request.form['lab_description']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file_pdf(file.filename):
            current_time = time.time()
            filename = str(int(current_time)) + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql = """
            INSERT INTO basic_labs (basic_lab_name, basic_lab_description, basic_lab_file_name) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (lab_name, lab_description, filename))
            conn.commit()
            return redirect(url_for('home'))
    return render_template("create_lab.html")

@app.route("/update_lab/<lab_id>", methods=['GET', 'POST'])
def update_lab(lab_id):
    print(lab_id)
    sql = """
    SELECT * FROM basic_labs WHERE basic_lab_id = %s
    """
    cursor.execute(sql, lab_id)
    data = cursor.fetchone()
    return render_template("update_lab.html", data=data, lab_id=lab_id)

@app.route("/all_labs")
def all_labs():
    if "email" in session:
        sql = """\
        SELECT * FROM basic_labs\
        """
        cursor.execute(sql)
        datas = cursor.fetchall()
        return render_template("lab_all.html", datas=datas)
    return redirect(url_for("login"))


# @app.route("/all_testcase/<lab_id>")
# def all_testcase(lab_id):
#     sql = """\
#     SELECT * FROM basic_labs\;
#     """


@app.route("/add_testcase/<lab_id>", methods=['GET', 'POST'])
def add_testcase(lab_id):
    UPLOAD_FOLDER = '/home/BUU/64160038/Basic/static/labs/testcase'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if "email" in session:
        if request.method == "POST":
            # print(request.files)
            input_file = []
            output_file = []
            for i in request.files:
                # print(i)
                file = request.files[i]
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file_txt(file.filename):
                    current_time = time.time()
                    filename = str(int(current_time)) + secure_filename(file.filename)
                    if "input" in i:
                        input_file.append(filename)
                    elif "output" in i:
                        output_file.append(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql = """
            INSERT INTO basic_lab_testcase (basic_lab_id, basic_input_path, basic_output_path)
            VALUES (%s, %s, %s)
            """
            for i in range(len(input_file)):
                cursor.execute(sql, (lab_id, input_file[i], output_file[i]))
                conn.commit()
        return render_template("add_testcase.html")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
