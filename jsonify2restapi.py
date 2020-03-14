import re
import requests
import json
import os


dir ="/home/vcarceler/desarrollo/jsonify2restapi/content-import"
url = 'http://10.231.51.229:8080'

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
            print(" - Type: " + data["_type"])
