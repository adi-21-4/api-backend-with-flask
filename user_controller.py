from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, send_file, jsonify
from datetime import datetime
obj = user_model()
auth = auth_model()

@app.route("/user/getall", methods=["GET"])
@auth.token_auth("/user/getall")
def user_getall_controller():
    return obj.user_getall_model ()

@app.route("/user/addone", methods=["POST"])
@auth.token_auth("/user/addone")
def user_addone_controller():
    return obj.user_addone_model (request.form)

@app.route("/user/update", methods=["PUT"])
@auth.token_auth("/user/update")
def user_update_controller():
    return obj.user_update_model (request.form)

@app.route("/user/delete/<id>", methods=["DELETE"])
@auth.token_auth("/user/delete/<id>")
def user_delete_controller(id):
    return obj.user_delete_model (id)

@app.route("/user/patch/<id>", methods=["PATCH"])
@auth.token_auth("/user/patch/<id>")
def user_patch_controller(id):
    return obj.user_patch_model (request.form, id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods=["GET"])
@auth.token_auth("/user/getall/limit/<limit>/page/<page>")
def user_pagination_controller(limit, page):
    return obj.user_pagination_model (limit, page)

@app.route("/user/<uid>/upload/avatar", methods=["PUT"])
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    UniqueFileName = str(datetime.now().timestamp()).replace(".","")
    FileNameSplit = file.filename.split(".")
    ext = FileNameSplit[len(FileNameSplit)-1]
    FinalFilePath = f"uploads/{UniqueFileName}.{ext}"
    file.save(FinalFilePath)
    return obj.user_upload_avatar_model(uid, FinalFilePath)

@app.route("/uploads/<filename>", methods=["GET"])
def user_getavatar_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login", methods=["POST"])
def user_login_controller():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    return obj.user_login_model(data)
