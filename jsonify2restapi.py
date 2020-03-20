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
error_log = "error.log"
imported_log = "imported.log"

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

    if "creators" in data:
        new_data['creators'] = data['creators']

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

    # File
    # En los datos a importar hay varios ficheros de imagen que no incluyen los datos (29.json, 30.json, 31, 32)
    # https://plonerestapi.readthedocs.io/en/latest/serialization.html#file-image-fields
    if "_datafield_file" in data:
        new_data['file'] = {}
        new_data['file']['data'] = data['_datafield_file']['data']
        new_data['file']['encoding'] = data['_datafield_file']['encoding']
        new_data['file']['filename'] = data['_datafield_file']['filename']
        new_data['file']['content-type'] = data['_datafield_file']['content_type']

    # Image
    # 39.json
    # /elpuig/Members/acanal8/noticies/2016-17/deures-destiu-per-als-alumnes-que-cursaran-primer-deso
    if "_datafield_image" in data:
        new_data['image'] = {}
        new_data['image']['data'] = data['_datafield_image']['data']
        new_data['image']['encoding'] = data['_datafield_image']['encoding']
        new_data['image']['filename'] = data['_datafield_image']['filename']
        new_data['image']['content-type'] = data['_datafield_image']['content_type']

    # Link
    # 994.json
    if "remoteUrl" in data:
        new_data['remoteUrl'] = data['remoteUrl']

    # post data to plonerestapi
    url_post = url + data['_path'][0:data['_path'].rfind('/')]
    #logger.debug("url_post: " + url_post)
    r = requests.post(url_post,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        json=new_data,
        auth=(plone_user, plone_password))

    if r.status_code != 201:
        logger.error(str(r.status_code) + ":" + " type: " + new_data['@type'] + " id: " + new_data['id'] + " " + filename)

        error = {}
        error['status_code'] = r.status_code
        error['type'] = new_data['@type']
        error['url_post'] = url_post
        error['id'] = new_data['id']
        error['filename'] = filename
        error_log_file.write(json.dumps(error) + "\n")
        #logger.error(new_data)
        
    else:
        logger.info("Ok - " + url_post)
        #print(r.text)

        imported = {}
        imported['type'] = new_data['@type']
        imported['url_post'] = url_post
        imported['id'] = new_data['id']
        imported['filename'] = filename
        imported_log_file.write(json.dumps(imported) + "\n")
        
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

            #print(r.status_code)
            #print(r.text)




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

        with open(filename, "r") as json_file, open(error_log, "a") as error_log_file, open(imported_log, "a") as imported_log_file:
            data = json.load(json_file)

            import_content(data)
            

    