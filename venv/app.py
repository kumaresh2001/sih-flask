from distutils.debug import DEBUG
from pickle import TRUE
from flask import Flask
import sqlite3
from flask_cors import CORS
import json
import numpy as np
import tensorflow
from flask import request
from keras.models import load_model
from pymongo import MongoClient

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

@app.route('/other', methods=['GET', 'POST'])
def parse_request():
    model = load_model(r'D:\SIH\sih-flask/venv/my_model.h5')
    data = request.data 
    dict = json.loads(data)
    numpy_arrays = np.array(dict["answers"]["answers"])
    numpy_2d_array = numpy_arrays.reshape(1,50)
    result = model.predict(numpy_2d_array)
    ocean = result[0].astype(int)
    ocean = ocean.tolist()
    profession = result[1]>0.5
    profession = profession.tolist()
    stream = result[2]>0.5
    stream = stream.tolist()
    return {"ocean":ocean,"stream":stream,"profession":profession}
    # return {"data":"Hello"}


@app.route('/login', methods=['GET', 'POST'])
def index():
    cluster = MongoClient("")
    requestData = json.loads(request.data)
    print(requestData)
    db = cluster["meraki"]
    collection = db["login"]
    loginFind = collection.find_one({"name":requestData["name"]},{"_id":0})
    if(loginFind==None):
        return({"notFound":"Username does not exists"})
    return(loginFind)

@app.route('/register',methods=['GET','POST'])
def register():
    cluster = MongoClient("")
    db = cluster["meraki"]
    collection = db["login"]
    requestData = json.loads(request.data)
    print(requestData)
    collection.insert_one(requestData)
    return("You have registered")

if __name__ == "__main__":
    app.run(debug=True)




# @app.route('/')
# def hello():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     #cur.execute("create table login (username TEXT PRIMARY KEY,name TEXT,password TEXT,student BOOLEAN)")
#     cur.execute("INSERT INTO login VALUES(?,?,?,?)",("suraj123","jef","password",1))
#     cur.execute("create table student (username TEXT,higher BOOLEAN,O INT,C INT,E INT,A INT,N INT)")
#     cur.execute("INSERT INTO student VALUES(?,?,?,?,?,?,?)",("suraj123",2,10,20,30,40,50))
#     cur.execute("create table lower (username TEXT,stream TEXT,diploma TEXT)")
#     cur.execute("INSERT INTO lower VALUES(?,?,?)",("suraj123","computers science","none"))
#     cur.execute("create table higher (username TEXT,profession TEXT)")
#     cur.execute("INSERT INTO higher VALUES(?,?)",("suraj123","engineers"))
#     cur.execute("select * from lower")
#     conn.commit()
#     row = cur.fetchall()
#     print(row[0]["username"])
#     conn.close()
#     return "oh no"

# @app.route('/insertValue')
# def secondPage():
#     x = '{"data":"hello"}'
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     #cur.execute("insert into login values(?,?,?)",("kumar","kumaresh","password"))
#     conn.commit() 
#     cur.execute("select * from login")
#     rows = cur.fetchall()
#     conn.close()
#     return rows[0]["name"]

