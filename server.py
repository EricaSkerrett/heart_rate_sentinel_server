from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

p_id = 0
email = "string"
p_age = 0 
p_hr = 0


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    # initialize patient and accept future HR measurements
    r = request.get_json()
    p_id = r.get("patient_id")
    email = r.get("attending_email")
    p_age = r.get
    p_hr = []
    return p_id, email, p_age, p_hr


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate_store():
    # store HR measurement for user with that email; include current time stamp
    r = request.get_json()
    if r.get("patient_id") == p_id:
        p_hr.append(r.get("heart_rate"))
    return p_hr


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    # return whether patient is currently tachycardic based on "previously/
    #  available heart rate? and return time stamp of most recent heart rate
    if patient_id == p_id:
        status = is_tachycardic(p_hr, p_age)
        print(status)
    else:
        print("This patient is not in the system")
    return


def is_tachycardic(p_hr, p_age):
    last_p_hr = 
    if p_age > 15 and p_hr > 100:
        status = "Tachycardic"
    else:
        status = "Not Tachycardic"
    return status


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate(patient_id):
    # return all the previous heart rate measurements for that patient
    dict = {
        "patient_id": p_id,
        "hr_list": p_hr,
    }
    return jsonify(dict)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def average(patient_id):
    # return the patient's average heart rate over all measurements
    # that are stored for this user
    avg_hr = np.mean(p_hr)
    return jsonify(avg_hr)


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
