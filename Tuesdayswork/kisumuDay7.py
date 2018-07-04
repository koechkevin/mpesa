
from flask import request,Flask,json,jsonify,Request,session
app=Flask(__name__)
app.secret_key="koech"
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
    if session[username]:
        return jsonify({"message": "You are already on session"})
    else:
        if username in info:
            if password==info[username]["password"]:
                session[username]=True
                return jsonify({"message": "Login successful"})
            else:
                return jsonify({"message": "Login unsuccessful wrong password"})
        else:
            return jsonify({"message": "Login unsuccessful wrong username"})
@app.route("/post_comment",methods=["GET","POST"])
def post_comment():
    if session[request.get_json()["username"]]:
        comment=request.get_json()["comment"]
        store_comments.append(comment)
        return jsonify({"message": "successful commenting"})
    else:
        return jsonify({"Alert":"please Login First"})
@app.route("/view_comments",methods=["POST","GET"])
def view_comments():
    username=request.get_json()["username"]
    if session[username]:
        output={}
        for each in store_comments:
            output.update({store_comments.index(each):each})
        return jsonify(output)
    else:
        return jsonify({"Alert":"please Login First"}) 
@app.route("/account_details",methods=["POST","GET"])   
def account_details():
    username=request.get_json()["username"]
    if username in info:
        if session[username]:
            return jsonify(info[username])
        else:
            return jsonify({"Alert":"please Login First"}) 
    else:
        return jsonify({"Alert":"please Register First"})
@app.route("/delete_comment/<int:commentID>",methods=["DELETE"])
def delete_comment(commentID):
    del store_comments[commentID]
    return jsonify({"Alert":"successfully deleted"})
           
if __name__=='__main__':
    app.run(port=5555,debug=True)     