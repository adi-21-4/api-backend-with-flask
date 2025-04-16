from functools import wraps
import mysql.connector
import json
from flask import make_response, request
import jwt
import re

class auth_model():
    def __init__(self):
        #connection estb code
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="aditya214",database="flask_tutorial")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except:
            print("Some error")

    
    def token_auth(self, endpoint):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwtdecoded = jwt.decode(token,"aditya",algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR":"TOKEN_EXPIRED"}, 404)
                    role_id = jwtdecoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint = '{endpoint}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        allowed_roles = json.loads(result[0]['roles'])
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                             return make_response({"ERROR":"INVALID_ROLE"}, 404)
                    else:
                        return make_response({"ERROR":"UNKNOWN_ENDPOINT"}, 404)
                else:
                    return make_response({"ERROR":"INVALID_TOKEN"}, 401)                
            return inner2
        return inner1