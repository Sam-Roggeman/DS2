import requests
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# The Username & Password of the currently logged-in User
username = None
password = None

session_data = dict()


def save_to_session(key, value):
    session_data[key] = value


def load_from_session(key):
    return session_data.pop(key) if key in session_data else None  # Pop to ensure that it is only used once


@app.route("/")
def feed():
    # ================================
    # FEATURE 9 (feed)
    #
    # Get the feed of the last N activities of your friends.
    # ================================

    global username

    N = 10

    if username is not None:
        feed = requests.get("http://feed:5000/activities/", params={"username": username, "number_of_activities": N}).json()
    else:
        feed = []

    return render_template('feed.html', username=username, password=password, feed=feed)


@app.route("/catalogue")
def catalogue():
    songs = requests.get("http://songs:5000/songs").json()

    return render_template('catalogue.html', username=username, password=password, songs=songs)


@app.route("/login")
def login_page():
    success = load_from_session('success')
    return render_template('login.html', username=username, password=password, success=success)


@app.route("/login", methods=['POST'])
def actual_login():
    req_username, req_password = request.form['username'], request.form['password']

    # ================================
    # FEATURE 2 (login)
    #
    # send the username and password to the microservice
    # microservice returns True if correct combination, False if otherwise.
    # Also pay attention to the status code returned by the microservice.
    # ================================
    success = requests.post("http://users:5000/users/login",
                            json={"username": req_username, "password": req_password}).json()
    save_to_session('success', success)
    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect('/login')


@app.route("/register")
def register_page():
    success = load_from_session('success')
    return render_template('register.html', username=username, password=password, success=success)


@app.route("/register", methods=['POST'])
def actual_register():
    req_username, req_password = request.form['username'], request.form['password']

    # ================================
    # FEATURE 1 (register)
    #
    # send the username and password to the microservice
    # microservice returns True if registration is succesful, False if otherwise.
    #
    # Registration is successful if a users with the same username doesn't exist yet.
    # ================================
    success = requests.post("http://users:5000/users/register",
                            json={"username": req_username, "password": req_password}).json()

    save_to_session('success', success)

    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect('/register')


@app.route("/friends")
def friends():
    success = load_from_session('success')
    global username
    # ================================
    # FEATURE 4
    #
    # Get a list of friends for the currently logged-in users
    # ================================
    friend_list = []
    if username is not None:
        friend_list = requests.get("http://friends:5000/friends", params={"username": username}).json()
    return render_template('friends.html', username=username, password=password, success=success,
                           friend_list=friend_list)


@app.route("/add_friend", methods=['POST'])
def add_friend():
    # ==============================
    # FEATURE 3
    #
    # send the username of the current users and the username of the added friend to the microservice
    # microservice returns True if the friend request is successful (the friend exists & is not already friends), False if otherwise
    # ==============================

    global username
    req_username = request.form['username']
    if username is not None:
        success = requests.post("http://friends:5000/friends/add",
                                json={"username1": username, "username2": req_username}).json()
        save_to_session('success', success)
    return redirect('/friends')


@app.route('/playlists')
def playlists():
    global username

    my_playlists = []
    shared_with_me = []

    if username is not None:
        # ================================
        # FEATURE
        #
        # Get all playlists you created and all playlist that are shared with you. (list of id, title pairs)
        # ================================

        my_playlists = requests.get("http://playlists:5000/playlists", params={"username": username}).json()
        shared_with_me = requests.get("http://playlists:5000/playlists/shared", params={"username": username}).json()

    return render_template('playlists.html', username=username, password=password, my_playlists=my_playlists,
                           shared_with_me=shared_with_me)


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    # ================================
    # FEATURE 5
    #
    # Create a playlist by sending the owner and the title to the microservice.
    # ================================
    global username
    title = request.form['title']

    requests.post("http://playlists:5000/playlists/create", json={"username": username, "title": title})

    return redirect('/playlists')


@app.route('/playlists/<int:playlist_id>')
def a_playlist(playlist_id):
    # ================================
    # FEATURE 7
    #
    # List all songs within a playlist
    # ================================
    songs = requests.get(f"http://playlists:5000/playlists/{playlist_id}").json()

    return render_template('a_playlist.html', username=username, password=password, songs=songs,
                           playlist_id=playlist_id)


@app.route('/add_song_to/<int:playlist_id>', methods=["POST"])
def add_song_to_playlist(playlist_id):
    # ================================
    # FEATURE 6
    #
    # Add a song (represented by a title & artist) to a playlist (represented by an id)
    # ================================
    title, artist = request.form['title'], request.form['artist']
    global username

    requests.post("http://playlists:5000/playlists/add_song",
                  json={"playlist_id": playlist_id,
                        "title": title, "artist": artist, "username": username})

    return redirect(f'/playlists/{playlist_id}')


@app.route('/invite_user_to/<int:playlist_id>', methods=["POST"])
def invite_user_to_playlist(playlist_id):
    # ================================
    # FEATURE 8
    #
    # Share a playlist (represented by an id) with a users.
    # ================================
    global username
    recipient = request.form['user']
    requests.put(f"http://playlists:5000/playlists/{playlist_id}/invite", params={"username": recipient, "username_owner": username})
    return redirect(f'/playlists/{playlist_id}')


@app.route("/logout")
def logout():
    global username, password

    username = None
    password = None
    return redirect('/')
