
from flask import request,Flask,json,jsonify,Request,session,make_response
import jwt

import datetime
from functools import wraps
app=Flask(__name__)
app.config['SECRET_KEY']="koech"
info={}
store_comments=[]

@app.route("/")
def Homepage():
    return jsonify({"message":"Please Register and login to continue"})
@app.route("/register" ,methods=['POST'])
def register():
    fname=request.get_json()["Fname"]
    lname=request.get_json()["Lname"]
    email=request.get_json()["email"]
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    info.update({username:{"first name":fname,"last name":lname,"email":email,"password":password}})
    session[username]=False
    if username in info:
        return jsonify({"message": "Register successful"})
    else:
        return jsonify({"message": "Register unsuccessful try again"})
@app.route("/login",methods=["GET","POST"])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    access = request.authorization
    if password == info[username]["password"]:
        token = jwt.encode({"username":username,"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=5)},app.config['SECRET_KEY'])
        return jsonify({"token":token.decode('utf-8')})
    else:
        return jsonify({"message":"Invalid credentials"}) 
def authorize(t):
    @wraps(t)
    def decorated(*args,**kwargs):
        
        if request.args.get('token')=='':
            return jsonify({"Alert":'please login'})
        try:
            jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
        except:
            return jsonify({"Alert":'please login again'})
        return t(*args,**kwargs)
    return decorated
    
@app.route("/post_comment",methods=["GET","POST"])
@authorize
def post_comment():
    comment=request.get_json()["comment"]
    store_comments.append(comment)
    return jsonify({"message": "successful commenting"})
@app.route("/view_comments",methods=["POST","GET"])
@authorize
def view_comments():    
    output={}
    for each in store_comments:
        output.update({store_comments.index(each):each})
    return jsonify(output)
@app.route("/account_details",methods=["POST","GET"])
@authorize
def account_details():
    return jsonify(info)
@app.route("/delete_comment/<int:commentID>",methods=["DELETE"])
@authorize
def delete_comment(commentID):
    del store_comments[commentID]
    return jsonify({"Alert":"successfully deleted"})
           
if __name__=='__main__':
    app.run(port=5555,debug=True)     