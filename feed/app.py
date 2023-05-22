import requests
from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('description')
parser.add_argument('number_of_activities')

app = Flask("users")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="feed", user="postgres", password="postgres", host="feed_persistence")
        print("DB connection succesful")
    except psycopg2.OperationalError:
        import time
        time.sleep(1)
        print("Retrying DB connection")

def add_activity(username, description):
    cur = conn.cursor()
    # check if user exists
    if user_exists(username):
        cur.execute(f"INSERT INTO activity (username, description) VALUES ('{username}','{description}');")
        conn.commit()
        cur.close()
        return True
    return False
def user_exists(username):
    try:
        user_exists = requests.get("http://users:5000/users/exists/", params={"username": username}).json()
        return user_exists
    except:
        return False
    return False
def get_all_friends(username):
    try:
        friends = requests.get("http://friends:5000/friends/", params={"username": username}).json()
        return friends
    except:
        return False
    return False
def get_all_friend_activity(username, number_of_activities):
    try:
        cur = conn.cursor()
        if user_exists(username):
            friends = get_all_friends(username)
            cur.execute(f"""
                SELECT  TO_CHAR(created_at, 'YYYY/MM/DD HH24:MM:SS'), description,username
                FROM activity 
                WHERE username = ANY(%s) 
                ORDER BY created_at 
                DESC LIMIT {number_of_activities};
            """, friends)
            return cur.fetchall()
    except:
        return []
    return []
class AddActivity(Resource):
    def post(self):
        args = flask_request.json
        return add_activity(args["username"], args["description"] )

class AllFriendActivity(Resource):
    def get(self):
        args = flask_request.args
        return get_all_friend_activity(args["username"], args["number_of_activities"])

api.add_resource(AddActivity, '/activities/add/')
api.add_resource(AllFriendActivity, '/activities/', '/feed/')
