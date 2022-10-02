from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flaskext.mysql import MySQL
from flask_cors import CORS
import pymysql
app = Flask(__name__)
CORS(app)

app.secret_key = "mysecretkey"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '34.124.203.100'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'poonnachit'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin004@'
app.config['MYSQL_DATABASE_DB'] = 'basic'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logout")
def  logout():
    return render_template("index.html")
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

@app.route('/cont1')
def cont1():
    return render_template("cont1.html")

@app.route('/cont2')
def cont2():
    return render_template("cont2.html")

@app.route('/cont3')
def cont3():
    return render_template("cont3.html")

@app.route('/cont4')
def cont4():
    return render_template("cont4.html")

@app.route('/cont5')
def cont5():
    return render_template("cont5.html")

@app.route('/cont6')
def cont6():
    return render_template("cont6.html")

@app.route('/cont7')
def cont7():
    return render_template("cont7.html")

@app.route('/cont8')
def cont8():
    return render_template("cont8.html")



if __name__ == '__main__':
    app.run(debug=True)
