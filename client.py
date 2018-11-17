import requests

inputs = {
    "patient_id": "2",
    "attending_email": "erica.skerrett@duke.edu",
    "user_age": 67,
}
r = requests.post("http://127.0.0.1:5001/api/new_patient", json=inputs)


inputs2 = {
    "patient_id": "2",
    "heart_rate": 67,  # need to get time stamped heart rate
}
r = requests.post("http://127.0.0.1:5001/api/heart_rate", json=inputs2)


inputs3 = {
    "patient_id": "2",
    "heart_rate_average_since": "2018-03-09 11:00:36.372339"
}
r = requests.post("http://127.0.0.1:5001/api/heart_rate/interval_average", json=inputs3)
