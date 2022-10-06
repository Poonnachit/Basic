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
def logout():
    return render_template("index.html")


@app.route('/lesson/<lessonName>')
def lesson(lessonName):
    return render_template(lessonName+".html")


@app.route('/lab/<labName>')
def lab(labName):
    return render_template(labName+".html")


if __name__ == '__main__':
    app.run(debug=True)

