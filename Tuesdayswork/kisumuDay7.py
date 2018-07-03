
from flask import *
app=Flask(__name__)
app.secret_key="koech"
info={}
store_comments=[]
@app.route("/register" ,methods=['POST',"GET"])
def register():
    fname=request.get_json()["Fname"]
    lname=request.get_json()["Lname"]
    email=request.get_json()["email"]
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    info.update({username:{"first name":fname,"last name":lname,"email":email,"password":password}})
    return jsonify({"message": "Register successful"})
@app.route("/login",methods=["GET","POST"])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if username in info:
        if password==info[username]["password"]:
            session["logged_in"]=True
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Login unsuccessful wrong password"})
    else:
        return jsonify({"message": "Login unsuccessful wrong username"})
@app.route("/post_comment",methods=["GET","POST"])
def post_comment():
    comment=request.get_json()["comment"]
    store_comments.append(comment)
    return jsonify({"message": "successful commenting"})
@app.route("/view_comments",methods=["GET"])
def view_comments():
    output={}
    for each in store_comments:
        output.update({store_comments.index(each):each})
    return jsonify(output)
@app.route("/account_details",methods=["GET"])   
def account_details():
    return jsonify(info)
if __name__=='__main__':
    app.run(port=9383,debug=True)
    
        