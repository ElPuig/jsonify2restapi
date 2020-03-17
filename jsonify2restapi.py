#
# Tipos de documentos en plonerestapi
#
#   http http://10.231.51.229:8080/elpuig/@types Accept:application/json -a admin:UUXdbVpOxgRf
#   http http://10.231.51.229:8080/elpuig/@types/Document Accept:application/json -a admin:UUXdbVpOxgRf
#


import re
import requests
import json
import os

from logzero import logger


#dir = "/home/vcarceler/desarrollo/jsonify2restapi/content-import"
dir = "/home/vcarceler/Descargas/content_elpuig_2020-03-16-10-19-58"
url = 'http://10.231.51.229:8080'
plone_user = 'admin'
plone_password = 'UUXdbVpOxgRf'

# returns an integer from the filename
def get_int(filename):
    return int(re.sub("[^0-9]", "", filename))

# imports content (from jsonify) into new plone using plonerestapi
def import_content(data):
    new_data = {}
    new_data['@type'] = data['_type']
    new_data['id'] = data['_id']
    new_data['title'] = data['title']
    new_data['description'] = data['description']
    new_data['contributors'] = data['contributors']
    new_data['UID'] = data['_uid'] # No funciona
    new_data['created'] = data['creation_date'] # No funciona

    # Collection, Document, Event, News Item
    if "text" in data:
        new_data['text'] = data['text']

    # Event
    if "startDate" in data:
        new_data['start'] = data['startDate']
    if "endDate" in data:
        new_data['end'] = data['endDate']
    if "location" in data:
        new_data['location'] = data['location']
    if "attendees" in data:
        new_data['attendees'] = data['attendees']
    if "contactName" in data:
        new_data['contact_name'] = data['contactName']
    if "contactEmail" in data:
        new_data['contact_email'] = data['contactEmail']
    if "contactEmail" in data:
        new_data['contact_phone'] = data['contactPhone']
    if "eventUrl" in data and data['eventUrl'] != "": # plonerestapi no acepta una cadena vacía como event_url
        new_data['event_url'] = data['eventUrl']

    # post data to plonerestapi
    url_post = url + data['_path'][0:data['_path'].rfind('/')]
    logger.debug("url_post: " + url_post)
    r = requests.post(url_post,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        json=new_data,
        auth=(plone_user, plone_password))

    if r.status_code != 201:
        logger.error(str(r.status_code) + ":" + " id: " + new_data['id'] + " type: " + new_data['@type'] + " " + filename)
        logger.error(new_data)
        
    else:
        print(r.text)
        logger.info("Ok")
        # Se recorre el historial aplicando las fechas y los cambios de estado: published, private, pending
        for state in data['_workflow_history']['simple_publication_workflow']:
            
            method = "/@workflow/"
            
            if state['review_state'] == "published":
                method = method + "publish"

            if state['review_state'] == "private":
                method = method + "retract"

            if state['review_state'] == "pending":
                method = method + "submit"

            logger.debug("Change state: " + url + data['_path'] + method)

            history = {}
            history['comment'] = state['comments']
            history['effective'] = state['time']
            r = requests.post(url + data['_path'] + method,
                headers={'Accept': 'application/json'},
                auth=(plone_user, plone_password),
                json=history)

            print(r.status_code)
            print(r.text)




#
# Main script
#

logger.info("Content import directory: " + dir)
logger.info("Destination URL: " + url)

for d in sorted(os.listdir(dir), key=get_int):
    logger.info("Subdirectory: " + d)

    for f in sorted(os.listdir(dir + "/" + d), key=get_int):
        logger.info("File: " + f)

        filename = dir + "/" + d + "/" + f
        logger.info(" - Filename: " + filename)

        with open(filename, "r") as json_file:
            data = json.load(json_file)

            import_content(data)
            

    break