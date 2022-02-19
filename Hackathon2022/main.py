from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid
import random

app = Flask(__name__)
app.secret_key = "~!@#$%^&*()_+QWERASDFZXCV"

UPLOADED_FILE_DIR_PATH = os.path.join(os.path.dirname(__file__), "static", "uploaded-images")
UPLOADED_ICON_FILE_DIR_PATH = os.path.join(os.path.dirname(__file__), "static", "discord_server_icons")
DATA_BASE_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database3.sqlite')

def check_to_create_table():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Articles ( id INTEGER PRIMARY KEY, name TEXT , article_name TEXT , email TEXT , message TEXT )')

    connection.close()


def check_to_create_table_account_info():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Accounts ( id INTEGER PRIMARY KEY, username TEXT , email TEXT , password TEXT )')

    connection.close()

check_to_create_table()
check_to_create_table_account_info()

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/create_account')
def create_account():
    return render_template('create_account.html')


@app.route('/search')
def search():
    return render_template('search_for_art.html', records='')


@app.route('/search_results', methods=["POST"])
def search_results():
    requested_search = request.values.get("search_input")

    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "SELECT * FROM Articles WHERE name Like ? OR email Like ? OR article_name Like ?",
        (requested_search, requested_search, requested_search))
    records = cur.fetchall()

    connection.commit()
    connection.close()
    return render_template('search_for_art.html',
                           records=records)


@app.route('/about')
def about():
    return render_template('page2.html')

@app.route('/logged_in_confirmation')
def logged_in_confirmation():
    return render_template('logged_in_confirmation.html')


@app.route("/process", methods=["POST"])
def process():
    username = request.values.get("username")
    article_name = request.values.get("title")
    email = request.values.get('email')
    message = request.values.get('message')



    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO Articles(name, article_name, email, message) VALUES (?, ?, ?, ?)",
        (username, article_name, email, message))
    connection.commit()
    connection.close()
    return render_template("uploading_success.html",
                           username=username,
                           article_name=article_name,
                           email=email,
                           message=message)



@app.route("/details_of_article", methods=["POST", "GET"])
def article_details():
    requested_name = request.values.get('name')
    requested_article_name = request.values.get('article_name')
    requested_email = request.values.get('email')
    requested_message = request.values.get('message')


    return render_template('details_of_article.html',
                           requested_name=requested_name,
                           requested_article_name=requested_article_name,
                           requested_email=requested_email,
                           requested_message=requested_message)


@app.route('/action_page')
def action_page():
    username = request.values.get('username')
    email = request.values.get('email')
    password = request.values.get('psw')

    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO Accounts (username, email, password) VALUES (?, ?, ?)",
        (username, email, password))
    connection.commit()
    connection.close()

    return render_template('successful_account_creation.html')







@app.route("/login", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("sign_in.html", username="", error_message="")

    username = request.values.get("username")
    password = request.values.get("password")
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Accounts WHERE username=? and password=?", (username, password))
    one_user = cur.fetchone()

    if one_user is not None:
        # Put a new value into session
        session["logged_in_user"] = username
        connection.close()

        return redirect("/logged_in_confirmation")
    else:
        connection.close()
        return render_template("sign_in.html", username=username, error_message="Username or password is wrong!")

@app.route("/logged_out", methods=["POST", "GET"])
def logout():
    session.clear()
    return render_template("successfully_logged_out.html")


@app.route('/server_uploading')
def server_uploading():
    return render_template('secret_server_upload_page_discord_1280.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=3000, debug=True)