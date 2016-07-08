"""
    This file provides functions to read from brainParts.json into a python list.
    note: brainParts.json must be in the same folder as this script

    @author Justin Bonner
"""

"""
    Dictionary Format:

    "vtkFileName"
    "synonyms"
    "name"
    "containers"   a list of strings
    "subComponents"
"""
#python 2 or 3 compatable

import json
import os.path

JSON_FILE_PATH = "brainParts.json"

#loads the json entries into a list where each entry is a dictionary
def getJsonEntries():
    jsonFile = open(JSON_FILE_PATH, "r")
    rawJsonString = jsonFile.read()
    #print rawJsonString
    jsonData = json.loads(rawJsonString)
    jsonFile.close()
    return jsonData
    
    
#loads the json entries into a dictionary where each key links to a dictionary
def getSortedJsonEntries():
    jsonDict = dict()
    jsonList = getJsonEntries()
    for entry in jsonList:
        jsonDict[entry['name']] = entry
        for synonym in entry['synonyms']:
            jsonDict[synonym] = entry
    return jsonDict

