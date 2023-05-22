import requests
from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('username1')
parser.add_argument('username2')
parser.add_argument('username')

app = Flask("songs")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="friends", user="postgres", password="postgres", host="friends_persistence")
    except psycopg2.OperationalError:
        import time
        time.sleep(1)


def add_friend(username1, username2):
    try:
        cur = conn.cursor()
        user1_exists = requests.get("http://users:5000/users/exists/", params={"username": username1}).json()
        user2_exists = requests.get("http://users:5000/users/exists/", params={"username": username2}).json()



        added = username2 in all_friends(username1)
        if user1_exists and user2_exists and not added:
            cur.execute(f"INSERT INTO friends (username1, username2) VALUES ('{username1}','{username2}');")
            conn.commit()
            requests.post("http://feed:5000/activities/add/", json={"username": username1, "description": f"Added {username2} as a friend"})
            return True
    except:
        return False
    return False

def all_friends(username):
    try:
        curr = conn.cursor()
        user_exists = requests.get("http://users:5000/users/exists/", params={"username": username}).json()
        if user_exists:
            curr.execute(f"SELECT username2 FROM friends WHERE username1 = '{username}'")
            return curr.fetchall()
    except:
        return []
    return []
class AllFriends(Resource):
    def get (self):
        args = flask_request.args
        return all_friends(args['username'])
class AddFriend(Resource):
    def post(self):
        args = flask_request.json
        return add_friend(args['username1'], args['username2'])


api.add_resource(AddFriend, '/friends/add/')
api.add_resource(AllFriends, '/friends/')
