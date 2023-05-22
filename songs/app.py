from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('artist')

app = Flask("songs")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="songs", user="postgres", password="postgres", host="songs_persistence")
        print("DB connection succesful")
    except psycopg2.OperationalError:
        import time
        time.sleep(1)
        print("Retrying DB connection")


def all_songs(limit=1000):
    cur = conn.cursor()
    cur.execute(f"SELECT title, artist FROM songs LIMIT {limit};")
    return cur.fetchall()

def add_song(title, artist):
    if not song_exists(title, artist):
        cur = conn.cursor()
        cur.execute(f"INSERT INTO songs (title, artist) VALUES ({title}, {artist});")
        conn.commit()
        return True
    return False

def song_exists(title, artist):
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM songs WHERE title = '{title}' AND artist = '{artist}';", (title, artist))
    return bool(cur.fetchone()[0])  # Either True or False

class AllSongsResource(Resource):
    def get(self):
        return all_songs()

class SongExists(Resource):
    def get(self):
        args = flask_request.args
        return song_exists(args['title'], args['artist'])

class AddSong(Resource):
    def put(self):
        args = flask_request.args
        return add_song(args['title'], args['artist'])

api.add_resource(AllSongsResource, '/songs/')
api.add_resource(SongExists, '/songs/exist/')
api.add_resource(AddSong, '/songs/add/')
