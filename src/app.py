"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1) Get all family members:
@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    if members is None:
        raise APIException("No users found", 400)
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

# 2) Retrieve one member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_a_member(member_id):
    member = jackson_family.get_member(int(member_id))
    if member is None:
        raise APIException("This member does not exist", 400)
    response_body = {
        "member": member
    }
    return jsonify(response_body), 200

# 3) Add (POST) new member
@app.route('/member', methods=['POST'])
def add_a_member():
    try:
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", 400)
        if 'first_name' not in body:
            raise APIException("You need to specify a first name", 400)
        if 'age' not in body:
            raise APIException("You need to specify age", 400)
        try:
            float(body['age'])
        except ValueError:
            return jsonify('age must be a number', 400)
        if 'lucky_numbers' not in body:
            raise APIException("You need to specify lucky numbers", 400)
        new_member = {
            "first_name": body['first_name'],
            "age": body['age'],
            "lucky_numbers": body['lucky_numbers'],
            # "id": body['id']
        }
        jackson_family.add_member(new_member)
        return jsonify("Success", 200)
    except:
        return jsonify('ups!! something went wrong, try again', 400)

# 4) DELETE one member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_a_member(member_id):
    # search for this member
    member = jackson_family.get_member(int(member_id))
    if member is None:
        raise APIException("This member does not exist", 400)
    member = jackson_family.delete_member(member_id)
    response_body = "Success"
    return jsonify(response_body), 200

# 5) UPDATE one member
@app.route('/member/<int:member_id>', methods=['PUT'])
def update_a_member(member_id):
    body = request.get_json()
    member = jackson_family.get_member(member_id)
    try:
        if "first_name" in body:
                member["first_name"] = body["first_name"]
        if "age" in body:
                member["age"] = body["age"]
        if "lucky_numbers" in body:
                member["lucky_numbers"] = body["lucky_numbers"]
        return jsonify("Member Modified", 200)
    except:
        return jsonify("cannot proccess your request", 400)

    
# this only runs if `$ python src/app.py` is executed, these lines always go at the end
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
