# heart_rate_sentinel_server
Erica Skerrett

BME590.06

_Purpose_: Stores patient heart rate information on a remote server. Patients are identified based on their patient ID. When called, server checks last reading for tachycardia and sends alert email to attending. 

## Main Functions

* POST New patient: Records new patient ID, attending email, and patient age
* POST Store heart rate: Stores patient heart rate and time stamp every time a post request is sent to the server
* GET Patient status: Returns patient tachycardic status upon request from client and informs attending via email if tachycardic
    * Available at `http://127.0.0.1:5001/api/status/<INSERT PATIENT ID>`
* GET Return heart rate: returns all of a specified patient's heart rate (based on patient ID number)
    * Available at `http://127.0.0.1:5001/api/heart_rate/<INSERT PATIENT ID>`
* GET Average heart rate: returns average heart rate for a patient
    * Available at `http://127.0.0.1:5001/api/heart_rate/average/<INSERT PATIENT ID>`
* POST Interval heart rate: returns average heart rate over interval specified by the client

See "client.py" for information on how to send infornmation to the remote server for POST requests.





