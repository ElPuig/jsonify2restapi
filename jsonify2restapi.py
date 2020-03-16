import re
import requests
import json
import os

from logzero import logger


dir ="/home/vcarceler/desarrollo/jsonify2restapi/content-import"
url = 'http://10.231.51.229:8080'
plone_user = 'admin'
plone_password = 'UUXdbVpOxgRf'

# returns an integer from the filename
def get_int(filename):
    return int(re.sub("[^0-9]", "", filename))

print("Content import directory: " + dir)
print("Destination URL: " + url)

for d in sorted(os.listdir(dir), key=get_int):
    print("Subdirectory: " + d)

    for f in sorted(os.listdir(dir + "/" + d), key=get_int):
        print("File: " + f)

        filename = dir + "/" + d + "/" + f
        print(" - Filename: " + filename)

        with open(filename, "r") as json_file:
            data = json.load(json_file)

            new_data = {}
            new_data['@type'] = data['_type']
            new_data['title'] = data['title']
            new_data['id'] = data['_id']
            new_data['description'] = data['description']
            new_data['contributors'] = data['contributors']
            new_data['UID'] = data['_uid'] # No funciona
            new_data['created'] = data['creation_date'] # No funciona
            

            # post data to restapi
            #url_post = url + "/Plone"#+ data["_path"]
            url_post = url + data['_path'][0:data['_path'].rfind('/')]
            logger.debug("url_post: " + url_post)
            r = requests.post(url_post,
                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                json=new_data,
                auth=(plone_user, plone_password))

            if r.status_code != 201:
                logger.error(str(r.status_code) + ":" + " id: " + new_data['id'] + " type:" + new_data['@type'] + " " + filename)
                logger.error(new_data)
                break
            else:
                print(r.text)
                logger.info("Ok")
                # Si se trata de un elemento público hay que cambiar el estado
                logger.debug("Publico: " + url + data['_path'] + "/@workflow/publish")
                r = requests.post(url + data['_path'] + "/@workflow/publish",
                    headers={'Accept': 'application/json'},
                    auth=(plone_user, plone_password))

                print(r.status_code)
                print(r.text)