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

# endpoint to add a member 
@app.route('/member', methods=['POST'])
def add_a_member():
    response_body = "Bad request"
    code = 400
    try: 
        body = request.get_json()
        if 'first_name' not in body:
            raise ValueError("First name not in body")
            # add nested error handling
        if 'age' not in body:
            raise ValueError("Agenot in body")
        if 'lucky_numbers' not in body:
            raise ValueError("Lucky numbers not in body")
        
        member = {
            'first_name': body['first_name'],
            'age': body['age'],
            'lucky_numbers': body['lucky_numbers'],
        }
        if 'id' in body:
            member['id'] = body['id']
            
        jackson_family.add_member(member)
        # the response
        response_body = "Success"
        code = 200
    except Exception as e:
        # if e is ValueError:
        response_body = str(e)
        code = 400
    return jsonify(response_body), code
    

# this only runs if `$ python src/app.py` is executed, these lines always go at the end
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
