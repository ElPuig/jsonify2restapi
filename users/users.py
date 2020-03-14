import csv
import requests
import json

csvfilename = 'usuarios.csv'
url = 'http://192.168.17.111:8080/Plone/@users'
user = 'admin'
password = 'hW5yvGepwGVa'

def create_user(login, name, address, passw):
    data = {'email': address, 'fullname': name, 'password': passw, 'roles': ['Member'], 'username': login}
    print(data)
    r = requests.post(url,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        json=data,
        auth=(user, password))

    if r.status_code != 201:
        print(str(r.status_code) + " DATA: " + data)


with open(csvfilename, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        create_user(row[0], row[1], row[2], row[3])