import os
import shutil
import json
import __root__

from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import render_template

import requests
from werkzeug.utils import secure_filename
from pprint import pprint

from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

from Scripts.Services.Login_Register.register_login_services import User
from Scripts.Services.DatabaseConnection.crud_truckbook_db_v1 import TruckBookOperationCRUD
from Scripts.Services.DatabaseConnection.read_and_write_json_files import *
from Scripts.Services.Algorithms.BFS_shortest_path import CalculateShortestPath
from Constants import const
from Scripts.Utility import utils


exception_message = '{"status":False, "status":"Server error, please contact your administrator"}'
method_error_message = '{"status": False, "message": "Method not supported!"}'



app_main = Blueprint("truckbook_api", __name__)



##----------------------------------------------- APIs Security --------------------------------------------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if request.method == "GET":
            token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        elif request.method == "POST":
            headers = request.headers
            bearer = headers.get('Authorization')  # Bearer YourTokenHere
            token = bearer.split()[1].split(':')[1]  # YourTokenHere

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, utils.configuration['SECRET_KEY'], algorithms='HS256')
            print(data)
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app_main.route('/generate_key')
def generate_key():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({"user": auth.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=59)}, utils.configuration['SECRET_KEY'])
        print(token)
        return jsonify( {'token' : token} )


    return make_response("Could not verify!", 401, {"WWW-Authenticate" : "Basic realm='Login Required'"})


@app_main.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Implements signup functionality. Allows username i.e phone number and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores phone number and hashed password inside database.
    Username i.e phone number should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        try:
            phone_number = request.form['phone_number']
            password = request.form['password']

            if not (phone_number and password):
                print("Username or Password cannot be empty")
                return {"status": 0, "message": "Username or Password cannot be empty" }
            else:
                phone_number = phone_number.strip()
                password = password.strip()

            # # Returns salted pwd hash in format : method$salt$hashedvalue
            hashed_pwd = generate_password_hash(password, 'sha256')

            _user_obj = User(phone_number=phone_number, pass_hash=hashed_pwd)
            status = _user_obj.new_user_signup()

            response = {}
            response["status"] = status
            if status == 0:
                response["message"] = "user has already registered with the phone number: {}.".format(phone_number) + " Please login with the same number."
            elif status == 1:
                response["message"] = "user has successfully signed up with phone number: {}.".format(phone_number)

            return jsonify(response)

        except Exception as e:
            utils.logger.error("-Error--" + str(e))



@app_main.route("/login", methods=["GET", "POST"])
@token_required
def login():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        try:
            phone_number = request.form['phone_number']
            password = request.form['password']

            response = {}
            status = 0

            if not (phone_number and password):
                response['status'] = status
                response['message'] = "Please enter crendentials !!!"
            else:
                phone_number = phone_number.strip()
                password = password.strip()


            _user_obj = User(phone_number=phone_number, pass_hash=None)

            user_row_list = _user_obj.old_user_login(phone_number)
            if len(user_row_list) == 1:
                user_tuple = user_row_list[0]
                if user_tuple and check_password_hash(user_tuple[-1], password):
                    print("yes")
                    response['status'] = 1
                    response["message"] = "user with phone number {} has successfully logged in".format(phone_number)
                else:
                    response['status'] = -1
                    response["message"] = "Invalid username or password."

            elif len(user_row_list) == 0:
                response['status'] = 2
                response["message"] = "phone number {} is not yet signed up yet, please register register first".format(phone_number)

            return jsonify(response)

        except Exception as e:
            utils.logger.error("-Error--" + str(e))


@app_main.route("/change_phone", methods=["GET", "POST"])
@token_required
def update():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        try:
            phone_number = request.form['phone_number']
            password = request.form['password']

            response = {}
            status = 0

            if not (phone_number and password):
                response['status'] = status
                response['message'] = "Please enter crendentials !!!"
            else:
                phone_number = phone_number.strip()
                password = password.strip()

            _user_obj = User(phone_number=phone_number, pass_hash=None)

            user_row_list = _user_obj.old_user_login(phone_number)
            if len(user_row_list) == 1:
                user_tuple = user_row_list[0]
                if user_tuple and check_password_hash(user_tuple[-1], password):
                    print("yes")
                    response['status'] = 1
                    response["message"] = "user with phone number {} has successfully logged in".format(phone_number)
                else:
                    response['status'] = -1
                    response["message"] = "Invalid username or password."

            elif len(user_row_list) == 0:
                response['status'] = 2
                response["message"] = "phone number {} is not yet signed up yet, please register register first".format(phone_number)

            return jsonify(response)

        except Exception as e:
            utils.logger.error("-Error--" + str(e))


## ---------------------------------------------------------------------------------------------------------------------

@app_main.route("/create_master_database", methods=["GET", "POST"])
@token_required
def create_master_database():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        try:
            stationdb_obj = TruckBookOperationCRUD()

        except Exception as e:
            utils.logger.error("-Error--" + str(e))
## ---------------------------------------------------------------------------------------------------------------------


@app_main.route("/fetch_stations", methods=["GET", "POST"])
@token_required
def fetch_allstations():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "GET":
        try:
            all_intersections_list = fetch_all_stations_linewise(const.LineWiseStations_dir_path)


            for stations_lst in all_intersections_list:
                for k, v in stations_lst.items():
                    print(v)

            return jsonify(all_intersections_list)

        except Exception as e:
            utils.logger.error("-Error--" + str(e))


@app_main.route("/fetch_intersections", methods=["GET", "POST"])
@token_required
def fetch_intersections():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "GET":
        try:
            all_intersections_dict, all_intersections = fetch_all_intersections(const.LineWiseStations_dir_path)


            for i in all_intersections_dict:
                for k, v in i.items():
                    print(v)
            res = {}
            res['linewise_intersections_list'] = all_intersections_dict
            res['total_intersections_list'] = all_intersections
            return jsonify(res)

        except Exception as e:
            utils.logger.error("-Error--" + str(e))



@app_main.route("/shortest_path", methods=["GET", "POST"])
@token_required
def find_shortest_path():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        try:
            starting_node = request.form['starting_node'].lower()
            destination_node = request.form['destination_node'].lower()

            bfs_obj = CalculateShortestPath()
            res = bfs_obj.print_shortest_distance(starting_node, destination_node)

            return jsonify(res)


        except Exception as e:
            utils.logger.error("-Error--" + str(e))
