from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

app = Flask("users")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="users", user="postgres", password="postgres", host="users_persistence")
        print("DB connection succesful")
    except psycopg2.OperationalError:
        import time
        time.sleep(1)
        print("Retrying DB connection")

def user_exists(username):
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM users WHERE username = '{username}';")
    return bool(cur.fetchone()[0])  # Either True or False


def register(username, password):
    cur = conn.cursor()

    if not user_exists(username):
        cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');")
        conn.commit()
        return True
    return False

def login(username, password):
    cur = conn.cursor()
    if user_exists(username):
        cur.execute(f"SELECT password FROM users WHERE username = '{username}';")
        succ=  cur.fetchone()[0] == password
        return succ
    return False

class Login(Resource):
    def post(self):
        args = flask_request.get_json()
        return login(args["username"], args["password"])

class Register(Resource):
    def post(self):
        args = flask_request.get_json()
        return register(args["username"], args["password"])
class UserExists(Resource):
    def get(self):
        args = flask_request.args
        return user_exists(args['username'])
api.add_resource(Register, '/users/register/')
api.add_resource(Login, '/users/login/')
api.add_resource(UserExists, '/users/exists/')
