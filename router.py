""" router for SoundSystem web site """

from flask import (
    Flask, render_template, request, make_response,
    session, redirect, url_for, jsonify
)
from jinja2 import Environment
from datetime import timedelta
# from markupsafe import escape
from pkg_sound_system import DB_connect
import json
import os


app = Flask(__name__)
app.secret_key = "jonathan"
app.permanent_session_lifetime = timedelta(minutes=35)
env = Environment()


def count_file(folder):
    root = "/static/img/" + folder + "/"
    path = os.getcwd() + root
    list_of_files = {}
    for filename in os.listdir(path):
        fileWithoutExt = os.path.splitext(filename)[0]
        list_of_files[fileWithoutExt] = root + filename
    return list_of_files


def is_status(var):
    if var == 4:
        return 4
    else:
        if isinstance(var, str):
            return [1, var]
        if isinstance(var, bool):
            return 2 if var is True else 3


@app.template_filter('json_reverse')
def json_reverse(json_data):
    datapy = json.loads(json_data)
    return datapy


app.jinja_env.filters['json_reverse'] = json_reverse


@app.template_filter()
def session_exist(key):
    if key in session:
        return True
    return False


app.jinja_env.filters['sessxist'] = session_exist


obj_vars = {
    "sd_title": "SoundSystem",
    "file_presentation": count_file("bg_presentation"),
    "file_albums_img": count_file("albums_img")
}
db = DB_connect.db_conect()


@app.route('/')
@app.route('/index/')
def home_page():
    return render_template("index.html", obj_var=obj_vars)


@app.route('/go_search/', methods=['GET', 'POST'])
def go_search():
    if request.method == 'POST':
        if request.form == '':
            search = "zero"
        else:
            search = request.form['search']
        resp = db.get_search(search)
        if type(resp) is not bool and not False:
            return profile(resp)
        return redirect(url_for("home_page"))
    else:
        return redirect(url_for("login_page"))


@app.route('/login/')
def login_page():
    if "user" in session:
        return redirect(url_for("profile"))
    return render_template("login.html", obj_var=None)


@app.route('/logout/')
def logout():
    session.pop("user", None)
    return redirect(url_for("home_page"))


@app.route('/signup/')
def signup_page():
    return render_template("signup.html", obj_var=4)


@app.route('/conexion_page/', methods=['GET', 'POST'])
def conexion_page():
    if request.method == 'POST':
        result = request.form
        send = []
        for key in result:
            send.append(result[key])
        verif_log = db.login(send[0], send[1])
        if not verif_log:
            return render_template("login.html", obj_var="Retry later.")
        else:
            if is_status(verif_log[1]) == 2 or 3:
                if verif_log[1]:
                    session["user"] = send[0]
                    return redirect(url_for("profile", username=send[0]))
                else:
                    return render_template("login.html", obj_var=verif_log[0])


@app.route('/profile/')
def profile(albums_data=None):
    if "user" in session:
        if not albums_data:
            return render_template("profile.html", obj_var=None)
        else:
            return render_template("profile.html", obj_var=albums_data)
    return redirect(url_for("login_page"))


@app.route('/profile/create-playlist', methods=["POST"])
def create_playlist():
    if request.method == 'POST':
        result = request.get_json()
        data_song = []
        for song in result:
            filtred_song = json_reverse(song)
            data_song.append(filtred_song)
        if "user" in session:
            data_song.append({'user':session["user"]})
        else:
            print("cannot get user_session.")
        print(f"new create playlist \n{data_song=}")
        db.set_playlist(data_song)
        res = make_response(jsonify({"message": "JSON recieved"}), 200)
        return res


@app.route('/set_selected_album', methods=['POST'])
def set_selected_album():
    if request.method == 'POST':
        req = request.get_json()
        if "user" in session:
            req['user'] = session["user"]
        else:
            print("cannot get user_session.")
        print(f"result get by python {req=}")
        result = db.set_selected_album(req)
        print(f"{result=}")
        if result > 0:
            res = make_response(jsonify({"message": "OK"}), 200)
        else:
            res = make_response(jsonify({"message": "We got the data but there are PB with."}), 200)
        return res


@app.route('/inscription/', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        result = request.form
        send = []
        for key in result:
            send.append(result[key])
        # order data before sending ::
        # send[4], send[5], send[1], send[0], send[2], send[3]
        verif_signup = db.set_signup(
            send[4], send[5], send[1],
            send[0], send[2], int(send[3])
        )
        verif_status = is_status(verif_signup)
        return render_template("signup.html", obj_var=verif_status)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
