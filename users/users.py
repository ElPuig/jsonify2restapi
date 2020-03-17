import csv
import requests
import json

from logzero import logger

#csvfilename = 'usuarios.csv'
csvfilename = '/home/vcarceler/Descargas/usuarios.csv'
url = 'http://10.231.51.229:8080/elpuig/@users'
user = 'admin'
password = 'UUXdbVpOxgRf'

def create_user(login, name, address, passw):
    data = {'email': address, 'fullname': name, 'password': passw, 'roles': ['Member'], 'username': login}
    logger.info("Creating ... " + str(data))
    r = requests.post(url,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        json=data,
        auth=(user, password))

    if r.status_code != 201:
        logger.error(str(r.status_code) + " DATA: " + str(data))


with open(csvfilename, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        create_user(row[0], row[1], row[2], row[3])