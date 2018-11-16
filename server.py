from flask import Flask, jsonify, request
import numpy as np
import datetime

app = Flask(__name__)

global_M = {}
# Master dictionary to be filled with patients


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    # initialize patient and accept future HR measurements
    r = request.get_json()
    # need to check that this request is the correct format (using exception?)
    check = validate_post(r)
    if check == 0:
        # raise an exception for the user about input
        a = 1  # placeholder
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
    r = 1
    check = 1  # check is a boolean
    # may also want to check that the numbers aren't duplicated
    return check


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate_store():
    # store HR measurement for user with that email, include current time stamp
    r = request.get_json()
    stamp = datetime.datetime.now()
    check = validate_post(r)
    if check == 0:
        # raise an exception for the user about input
        a = 1  # placeholder
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
        status = is_tachycardic(last_p_hr, p_age)
    else:
        print("Patient not yet entered into system")
    return jsonify(status)  # return time stamp!
# Need to setup email


def is_tachycardic(last_p_hr, p_age):  # could maybe do @parametrize?

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
    return status


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
        p_hr = [x[0] for x in p_hr_tup]
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
