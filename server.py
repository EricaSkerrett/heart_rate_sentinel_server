from flask import Flask, jsonify, request
import numpy as np
import datetime
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)

global_M = {}
# Master dictionary to be filled with patients


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    # initialize patient and accept future HR measurements
    r = request.get_json()
    # need to check that this request is the correct format (using exception?)
    check = validate_post(r)
    print(check)
    if check == 0:
        # raise an exception for the user about input
        error = "inputs not entered correctly"  # placeholder
        print("inputs not entered correctly")
        return jsonify(error)
    p_id = r.get("patient_id")
    global global_M
    if p_id in global_M:
        print("patient already entered into system")
    else:
        global_M.update({p_id: r})
        hr = []
        p_info = global_M[p_id]
        p_info["heart_rate"] = hr
        global_M[p_id] = p_info
    print(global_M)
    return jsonify(p_id)  # not sure why I'm returning this...


def validate_post(r):
    temp = {
        "patient_id": "1",
        "attending_email": "user@duke.edu",
        "user_age": 1,
    }
    temp2 = {
        "patient_id": "1",
        "attending_email": "user@duke.edu",
        "user_age": 1,
        "heart_rate": [],
    }
    temp3 = {
            "patient_id": "1",
            "heart_rate": 400,  # need to get time stamped heart rate
        }
    if set(r.keys()) == set(temp.keys()) or set(r.keys()) == set(temp2.keys())\
            or set(r.keys()) == set(temp3.keys()):
        check = 1
    else:
        check = 0  # come back to fix this
    return check


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate_store():
    # store HR measurement for user with that email, include current time stamp
    r = request.get_json()
    stamp = datetime.datetime.now()
    check = validate_post(r)
    if check == 0:
        # raise an exception for the user about input
        error = "inputs not entered correctly"
        print("inputs not entered correctly")
        return jsonify(error)
    p_id = r.get("patient_id")
    p_hr = (r.get("heart_rate"), stamp)
    global global_M
    if p_id in global_M:
        p_info = global_M[p_id]
        p_info["heart_rate"].append(p_hr)
        global_M[p_id] = p_info
    else:
        print("Patient not yet entered into system")
    print(global_M)
    return jsonify(p_id)


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    # return whether patient is currently tachycardic based on "previously/
    #  available heart rate? and return time stamp of most recent heart rate
    global global_M
    p_id = patient_id
    if p_id in global_M:
        p_info = global_M[p_id]
        p_hr = p_info["heart_rate"]
        last_p_hr = p_hr[-1]
        print(last_p_hr)
        last_p_hr = last_p_hr[0]
        p_age = p_info["user_age"]
        status = is_tachycardic(last_p_hr, p_age, p_id)
    else:
        print("Patient not yet entered into system")
    return jsonify(status)  # return time stamp as well!
# Need to setup email


def is_tachycardic(last_p_hr, p_age, p_id):  # could maybe do @parametrize?

    if p_age < 1 and last_p_hr > 169:
        status = "Tachycardic"
    elif p_age <= 2 and last_p_hr > 151:
        status = "Tachycardic"
    elif p_age <= 4 and last_p_hr > 137:
        status = "Tachycardic"
    elif p_age <= 7 and last_p_hr > 133:
        status = "Tachycardic"
    elif p_age <= 11 and last_p_hr > 130:
        status = "Tachycardic"
    elif p_age <= 15 and last_p_hr > 119:
        status = "Tachycardic"
    elif p_age > 15 and last_p_hr > 100:
        status = "Tachycardic"
    else:
        status = "Not Tachycardic"
    if status == "Tachycardic":
        send_email(p_id)
    return status


def send_email(p_id):
    global global_M
    p_info = global_M[p_id]
    email = p_info["attending_email"]
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("erica.skerrett@duke.edu")
    to_email = Email(email)
    subject = "Tachycardic Patient"
    stamp = datetime.datetime.now()
    content = Content("text/plain", "Patient {}".format(p_id)+" is\
     tachycardic as of {}".format(stamp))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate(patient_id):
    # return all the previous heart rate measurements for that patient
    global global_M
    p_id = patient_id
    if p_id in global_M:
        p_info = global_M[p_id]
        p_hr = p_info["heart_rate"]
        dict = {
            "patient_id": p_id,
            "hr_list": p_hr,
        }
    else:
        dict = "ERROR: Patient not yet entered into system."
    return jsonify(dict)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def average(patient_id):
    # return the patient's average heart rate over all measurements
    # that are stored for this user
    global global_M
    p_id = patient_id
    if p_id in global_M:
        p_info = global_M[p_id]
        p_hr_tup = p_info["heart_rate"]
        print(p_hr_tup)
        p_hr = [x[0] for x in p_hr_tup]
        print(p_hr)
        avg_hr = find_avg(p_hr)
        dict = {
            "patient_id": p_id,
            "heart_rate_avg": avg_hr,
        }
    else:
        dict = "ERROR: Patient not yet entered into system."
    return jsonify(dict)


def find_avg(p_hr):
    avg_hr = np.mean(p_hr)
    return avg_hr


"""
@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average(p_id, ):
    output = {
        "patient_id": "1",
        "heart_rate_average_since": "2018-03-09 11:00:36.372339"
    }
    return jsonify(output)
"""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
