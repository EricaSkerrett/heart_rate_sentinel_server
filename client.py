import requests

inputs = {
    "patient_id": "1",
    "attending_email": "erica.skerrett@duke.edu",
    "user_age": 50,
}
r = requests.post("http://127.0.0.1:5001/api/new_patient", json=inputs)


inputs2 = {
    "patient_id": "1",
    "heart_rate": 100,  # need to get time stamped heart rate
}
r = requests.post("http://127.0.0.1:5001/api/heart_rate", json=inputs2)


# test get average
# validate post request
