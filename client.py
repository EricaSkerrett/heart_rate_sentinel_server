import requests

inputs = {
    "patient_id": "1",
    "attending_email": "suyash.kumar@duke.edu",
    "user_age": 50,
}
r = requests.post("http://127.0.0.1:5001/new_patient", json=inputs)
# how to put /api in url


inputs2 = {
    "patient_id": "1",
    "heart_rate": 100,
}
r = requests.post("http://127.0.0.1:5000/heart_rate", json=inputs2)
