import firebase_admin
import firebase_admin.db
from firebase_admin import credentials
import firebase_admin
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://smartattendance-5a59e-default-rtdb.firebaseio.com/"
})

ref = firebase_admin.db.reference('Students')

data = {
    "1": {
        "name": "Elon Musk",
        "branch" : "Computer Science",
        "batch" : 1999,
        "total_attendance" : 19,
        "standing" : "Good",
        "year" : 4,
        "last_attendacne_time" : "2022-11-12 00:54:34"
    } ,
   "2": {
        "name": "Ahmar Hasan Arish",
        "branch" : "Computer Science",
        "batch" : 2020,
        "total_attendance" : 39,
        "standing" : "Great",
        "year" : 4,
        "last_attendacne_time" : "2022-11-12 00:54:34"
    },
  "3": {
        "name": "James Bond",
        "branch" : "Detective Studies",
        "batch" : 2006,
        "total_attendance" : 5,
        "standing" : "Rogue",
        "year" : 20,
        "last_attendacne_time" : "2022-11-12 00:54:34"
    },
  "4": {
        "name": "Daemon Targaryen",
        "branch" : "Dragon Stone",
        "batch" : 2022,
        "total_attendance" : 15,
        "standing" : "Dangerous",
        "year" : 10,
        "last_attendacne_time" : "2022-11-12 00:54:34"
    },
  "5": {
        "name": "Renly Baratheon",
        "branch" : "King of Stormlands",
        "batch" : 2016,
        "total_attendance" : 55,
        "standing" : "Benevolent",
        "year" : 3,
        "last_attendacne_time" : "2022-10-12 00:54:34"
    },
    "6": {
        "name": "Aliza Hasan",
        "branch": "School",
        "batch": 2024,
        "total_attendance": 9,
        "standing": "Good",
        "year": 4,
        "last_attendacne_time": "2022-11-12 00:54:34"
    }
}

for key,value in data.items():
    ref.child(key).set(value)