from flask import Flask
import requests
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('artist')
parser.add_argument('username')
parser.add_argument('username_owner')
parser.add_argument('playlist_id')

app = Flask("songs")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="playlists", user="postgres", password="postgres", host="playlists_persistence")
        print("DB connection succesful")
    except psycopg2.OperationalError:
        import time
        time.sleep(1)
        print("Retrying DB connection")

def user_exists(username):
    try:
        user_exists = requests.get("http://users:5000/users/exists/", params={"username": username}).json()
        return user_exists
    except:
        return False
    return False
def song_exists(title, artist):
    try:
        song_exists = requests.get("http://songs:5000/songs/exist/", params={"title": title, "artist": artist}).json()
        return song_exists
    except:
        return False
    return False
def create_playlist(title,username):
    try:
        cur = conn.cursor()
        if user_exists(username):
            cur.execute(f"INSERT INTO playlists (title, username_owner) VALUES ('{title}','{username}');")
            conn.commit()
            requests.post("http://feed:5000/activities/add/", json={"username": username, "description": f"Created playlist {title}"})
            return True
    except:
        return False
    return False

def playlistExists(playlist_id):
    curr = conn.cursor()
    curr.execute(f"SELECT * FROM playlists WHERE playlist_id = {playlist_id};")
    return curr.fetchone() is not None
def all_songs_in_playlist(playlist_id):
    try:
        curr = conn.cursor()
        playlist_exists = playlistExists(playlist_id)
        if playlist_exists:
            curr.execute(f"SELECT title, artist FROM songInPlaylist WHERE playlist_id = {playlist_id};")
            return curr.fetchall()
    except:
        return []
    return []

def isOwnerOf(username, playlist_id):
    curr = conn.cursor()
    curr.execute(f"SELECT * FROM playlists WHERE username_owner = '{username}' AND playlist_id = {playlist_id};")
    return curr.fetchone() is not None

def add_song(title, artist, playlist_id, username):
    try:
        cur = conn.cursor()
        song_in_playlist = (title,artist) in all_songs_in_playlist(playlist_id)
        if playlistExists(playlist_id) and song_exists(title, artist) and not song_in_playlist and isOwnerOf(username, playlist_id):
            cur.execute(f"INSERT INTO songInPlaylist (playlist_id, artist,title) VALUES ({playlist_id},'{artist}','{title}');")
            conn.commit()
            requests.post("http://feed:5000/activities/add/", json={"username": username, "description": f"Added song {title} by {artist} to playlist {playlist_id}"})
            return True
    except:
        return False
    return False



def all_playlists(username):
    try:
        curr = conn.cursor()
        if user_exists(username):
            curr.execute(f"SELECT playlist_id,title FROM playlists WHERE username_owner = '{username}';")
            return curr.fetchall()
    except:
        return []
    return []

def all_shared_playlists(username):
    try:
        curr = conn.cursor()
        if user_exists(username):
            curr.execute(f"SELECT playlist_id, title FROM playlistSharedWith natural join playlists WHERE username = '{username}';")
            return curr.fetchall()
    except:
        return []
    return []
def invite_user(username, playlist_id, username_owner):
    try:
        curr = conn.cursor()
        if not user_exists(username) or not playlistExists(playlist_id) or isOwnerOf(username, playlist_id) or not isOwnerOf(username_owner, playlist_id):
            return False
        already_shared = (playlist_id,username) in all_shared_playlists(username)
        if already_shared:
            return False
        curr.execute(f"INSERT INTO playlistSharedWith (playlist_id, username) VALUES ({playlist_id},'{username}');")
        conn.commit()
        requests.post("http://feed:5000/activities/add/", json={"username": username_owner, "description": f"Shared playlist {playlist_id} with {username}"})
        return True
    except:
        return False
class CreatePlaylist(Resource):
    def post(self):
        args = flask_request.json
        return create_playlist(args['title'], args['username'])

class AllPlaylists(Resource):
    def get(self):
        args = flask_request.args
        return all_playlists(args['username'])

class AddSong(Resource):
    def post(self):
        args = flask_request.json
        return add_song(args['title'], args['artist'], args['playlist_id'], args['username'])
class AllSongsInPlaylist(Resource):
    def get(self, playlist_id):
        return all_songs_in_playlist(playlist_id)
class AllSharedPlaylists(Resource):
    def get(self):
        args = flask_request.args
        return all_shared_playlists(args['username'])
class InviteUser(Resource):
    def put(self, playlist_id):
        args = flask_request.args
        return invite_user(args['username'], playlist_id, args['username_owner'])

api.add_resource(CreatePlaylist, '/playlists/create/')
api.add_resource(AllPlaylists, '/playlists/','/playlists/owned/')
api.add_resource(AllSharedPlaylists, '/playlists/shared')
api.add_resource(AddSong, '/playlists/add_song/')
api.add_resource(AllSongsInPlaylist, '/playlists/<int:playlist_id>/')
api.add_resource(InviteUser, '/playlists/<int:playlist_id>/invite')