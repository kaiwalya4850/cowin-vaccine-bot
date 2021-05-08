import requests
import datetime
import json
import time
import google.cloud
import firebase_admin
from firebase_admin import credentials, firestore
import firestore_auth


cred = credentials.Certificate("check.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

doc = store.collection("Vaccine").document("Status")


doc.set({"First":"init"})
DIST_ID = 777
print_flag = 'y'

numdays = 5
age = 23

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

while(1):
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, date_str[0])
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(URL, headers=headers)
    if response.ok:
        resp_json = response.json()
        # print(json.dumps(resp_json, indent = 1))
        if resp_json["centers"]:
            #print("Available on: {}".format(date_str[0]))
            if(print_flag=='y' or print_flag=='Y'):
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age:
                            if((session["available_capacity"])==1):
                                y = True
                                doc.set({base:z})
                            else:
                                print("No",base)



        else:
            print("No available slots on {}".format(date_str[0]))
    time.sleep(30)
