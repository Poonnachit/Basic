from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flaskext.mysql import MySQL
from flask_cors import CORS
import pymysql
app = Flask(__name__)
CORS(app)

app.secret_key = "mysecretkey"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['MYSQL_DATABASE_USER'] = 'admin04'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin004'
app.config['MYSQL_DATABASE_DB'] = 'car_rental'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)


@app.route("/")
def home():
    # if "username" in session:
    # sql = "SELECT * FROM user"
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # name = session["name"]
    # email = session["email"]
    return render_template("index.html")
    # return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/action_login", methods=["POST"])
def action_login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        data = cursor.fetchone()
        if data:
            session["username"] = data["username"]
            session["name"] = data["name"]
            session["tel"] = data["tel"]
            session["email"] = data["email"]
            flash("login successful")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/action_register", methods=["POST"])
def action_register():
    if request.method == "POST":
        firstname = request.form["first_name"]
        lastname = request.form["last_name"]
        name = firstname+" "+lastname
        username = request.form["username"]
        password = request.form["password"]
        tel = request.form["tel"]
        email = request.form["email"]
        sql = "INSERT INTO user (name, username, password, tel, email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, username, password, tel, email))
        conn.commit()
        flash("Register successful")
        return redirect(url_for("login"))


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']
    sql = "INSERT INTO user (name, tel, email) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, tel, email))
    flash('User Added Successfully')
    conn.commit()
    return redirect(url_for('home'))


@app.route("/del_user/<id>", methods=['GET'])
def del_user(id):
    sql = "DELETE FROM user WHERE user_id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    flash('User Deleted Successfully')
    return redirect(url_for('home'))


@app.route('/edit_user/<id>', methods=['GET'])
def edit_user(id):
    sql = "SELECT * FROM user WHERE user_id = %s"
    cursor.execute(sql, (id,))
    data = cursor.fetchone()
    return render_template("edit.html", user=data)


@app.route('/update_user/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']
    sql = "UPDATE user SET name = %s, tel = %s, email = %s WHERE user_id = %s"
    cursor.execute(sql, (name, tel, email, id))
    flash('User Updated Successfully')
    conn.commit()
    return redirect(url_for('home'))


@app.route('/hel1')
def lesson1_1():
    return render_template("hel1.html")


@app.route('/hel2')
def lesson1_2():
    return render_template("hel2.html")


@app.route('/hel3')
def lesson1_3():
    return render_template("hel3.html")


@app.route('/hel4')
def lesson1_4():
    return render_template("hel4.html")


@app.route('/hel5')
def lesson1_5():
    return render_template("hel5.html")


@app.route('/hel6')
def lesson1_6():
    return render_template("hel6.html")


@app.route('/hel7')
def lesson1_7():
    return render_template("hel7.html")


@app.route('/hel8')
def lesson1_8():
    return render_template("hel8.html")


@app.route('/hel9')
def lesson1_9():
    return render_template("hel9.html")


@app.route('/hel10')
def lesson1_10():
    return render_template("hel10.html")


@app.route('/hel11')
def lesson1_11():
    return render_template("hel11.html")


@app.route('/hel12')
def lesson1_12():
    return render_template("hel12.html")


@app.route('/hel13')
def lesson1_13():
    return render_template("hel13.html")


@app.route('/hel14')
def lesson1_14():
    return render_template("hel14.html")


@app.route('/hel15')
def lesson1_15():
    return render_template("hel15.html")


@app.route('/lab_hel1')
def lab_hel1():
    return render_template("lab_hel1.html")


if __name__ == '__main__':
    app.run(debug=True)
