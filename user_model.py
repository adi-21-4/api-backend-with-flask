import mysql.connector
import json
from flask import make_response, jsonify
from datetime import datetime, timedelta
import jwt

class user_model():
    def __init__(self):
        #connection estb code
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="aditya214",database="flask_tutorial")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except:
            print("Some error")


#query exec code

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"payload":result}, 200) #successful
        else:
            return make_response({"message":"No data found"}, 204) #no data
        

    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO users(name ,email ,phone ,role ,password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')")
        return make_response({"message":"User created successfully"}, 201) #created
    
    
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}' ,email='{data['email']}' ,phone='{data['phone']}' ,role='{data['role']}' ,password='{data['password']}' WHERE id={data['id']} ")
        if self.cur.rowcount>0:
            return make_response({"message":"User updated successfully"}, 201) #created
        else:
            return make_response({"message":"Nothing to update"}, 202) #accepted but no processing need
        
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User deleted successfully"}, 200) #successful
        else:
            return make_response({"message":"Nothing to delete"}, 202) #accepted
        

    def user_patch_model(self, data, id):
        qry = "UPDATE users SET "#WHERE id={id}
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id={id}"
        self.cur.execute(qry)

        if self.cur.rowcount>0:
            return make_response({"message":"User updated successfully"}, 201) #created
        else:
            return make_response({"message":"Nothing to update"}, 202) #accepted but no processing need
        

    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"payload":result, "page_no":page, "limit":limit}, 200) #successful
        else:
            return make_response({"message":"No data found"}, 204) #no data


    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"File uploaded successfully"}, 201) #created
        else:
            return make_response({"message":"Nothing to update"}, 202) #accepted but no processing need
        

    def user_login_model(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return make_response(jsonify({"error": "Email and password are required"}), 400)

        self.cur.execute("SELECT id, name, email, avatar, role_id FROM users WHERE email=%s AND password=%s", (email, password))
        result = self.cur.fetchall()

        if not result:
            return make_response(jsonify({"error": "Invalid email or password"}), 401)

        userdata = result[0]

        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())

        payload = {
            "payload": userdata,
            "exp": exp_epoch_time
        }

        jwt_token = jwt.encode(payload, "aditya", algorithm="HS256")
        return make_response({"access_token": jwt_token}, 200)