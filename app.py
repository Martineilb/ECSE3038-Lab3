from flask import Flask, request, jsonify
from datetime import datetime
from flask_pymongo import PyMongo
from marshmallow import Schema, fields
from bson.json_util import dumps
from json import loads
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_CONNECTION_STRING")
mongo = PyMongo(app)

global now
now = datetime.now()
FAKE_DATABASE = []
profile_database = {}

profile_object = {}
count = 0
print(now)


#CREATE -- POST FUNCTIONS
@app.route("/profile", methods=["POST"])
def post():

    global u
    global f
    global r

    u = request.json["Username"]
    f = request.json["Colour"]
    r = request.json["Role"]   

    global profile_object
    profile_object = {
        "Last Updated": now,
        "Username": u,
        "Role": r,
        "Colour": f
    }
    return jsonify(profile_object)

#--------------TANK--------------------------

class DataSchema(Schema):
    location = fields.String(required=True)
    percent = fields.Integer(required=True)
    latitude = fields.Integer(required=True)
    longitude = fields.Integer(required=True)


@app.route("/data", methods=["POST"])
def post_data():

    request_dict = request.json
    new_data = DataSchema().load(request_dict)

    data_document = mongo.db.info.insert_one(new_data)
    data_id = data_document.inserted_id

    data = mongo.db.fruits.find_one({"_id": data_id})

    data_json = loads(dumps(data))

    return jsonify(data_json)


#READ --GET FUNCTIONS
@app.route("/profile", methods=["GET"])
def get_profile():
    global profile_object
    return jsonify(profile_object)

#-----------TANK------------------
@app.route("/data", methods=["GET"])
def get_data():
    info = mongo.db.info.find()
    data_list = loads(dumps(info))
    return jsonify(data_list)
  

#UPDATE -- PATCH FUNCTIONS
@app.route("/profile/<Username>/<Role>/<Colour>", methods=["PATCH"])
def patch_profile(Username, Role, Colour):


    global profile_object
    profile_database = [profile_object]
    #return jsonify(profile_object)
    
    #for u in profile_database:
    if 'Username' in request.json:
        profile_object["Username"] = request.json["Username"]
        return jsonify(profile_database)
    else:    
        #for r in profile_database:
        if 'Role' in request.json:
            profile_object["Role"]=request.json["Role"]  
            return jsonify(profile_database)
        else:   
            #for f in profile_database:
            if 'Colour' in request.json:
                profile_object["Colour"] = request.json["Colour"]
                        
                return jsonify(profile_database)
                                

#-----------------TANK_-----------------
@app.route("/data/<ObjectId:id>", methods=["PATCH"])
def update_data(id): 
    mongo.db.info.update_one({"_id":id}, {"$set": request.json})

    data = mongo.db.info.find_one({"_id":id})
    return jsonify(data_json)


#DELETE

@app.route("/data/<ObjectId:id>", methods=["DELETE"])
def delete_data(id):
    result = mongo.db.info.delete_one({"_id":id})

    if result.deleted_count == 1:
        return {
            "success": True
        }
    else:
        return{
            "success": False
        }, 400 



if __name__ == '__main__':
    app.run(
        debug=True,
        port=3000,
        host="0.0.0.0"
    )
 