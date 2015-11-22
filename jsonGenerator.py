"""
    This script converts files from the old neurolex format to a new json based format.
    It also uses a name matching strategy to try and match the file to a vtk model, not 100% effective.
    The matching will need to be improved.
    The file paths are currently hardcoded, not a huge issue as this script will only need to convert files once.
"""

import json
import os.path

#the file path to the folder containing neurolex text files
NEUROLEX_FOLDER_PATH = "/home/justin/Documents/pythonProjects/JsonGenerator/neurolex"

#the file path to the folder containing vtk model files
VTK_MODELS_FOLDER_PATH = "/home/justin/Documents/pythonProjects/JsonGenerator/models"

#the file path in which the Json will be written
JSON_PATH = "/home/justin/Documents/pythonProjects/JsonGenerator"

#the minimum similarity between a neurolex name and a vtk file name for identification
MIN_SIMILARITY = .75

#reads the neurolex text files and puts each line in a list
def getNeurolexList():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #neurolex text files are A.txt, B.txt etc.
    neurolexList = list()
    for i in range (len(alphabet)):
        fileName = NEUROLEX_FOLDER_PATH + "/" + alphabet[i] + ".txt"
        if not os.path.isfile(fileName):
            continue
        f = open(fileName, "r")
        for line in f:
            line = line.replace("\r", "").replace("\n", "").lower() #remove \r\n from line and make lower case
            neurolexList.append(line)
    return neurolexList

#a list of the raw sources of the neurolex text files appended together in alphabetical order
RAW_NEUROLEX_LIST = getNeurolexList()


#create a dictionary mapping string brain part names to the line number in which they appear in RAW_NEUROLEX_LIST
def createNeurolexDictionary():
    neurolexDictionary = dict()
    for i in range (len(RAW_NEUROLEX_LIST)):
        line = RAW_NEUROLEX_LIST[i]
        if (line == "") or (line[0] == "\t"):
            continue
        neurolexDictionary[line] = i
        synonymLine = RAW_NEUROLEX_LIST[i + 3].replace("\t3.  synonyms : ", "")
        if (synonymLine == "na") or (synonymLine == ""):
            continue
        for synonym in synonymLine.split(", "):
            if(synonym == ""):
                continue
            neurolexDictionary[synonym] = i
    return neurolexDictionary

#a dictionary mapping string brain part names to their index in RAW_NEUROLEX_LIST
NEUROLEX_DICTIONARY = createNeurolexDictionary()

#returns a list of the model file names in the specified directory
def getVtkModelsList(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError("File not found:  " + filePath)
    return os.listdir(filePath)


def estimateNeurolexName(vtkFileName):
    nameAsList = vtkFileName.replace(".vtk", "").split("_")
    del nameAsList[0]
    del nameAsList[0]
    vtkName = " ".join(nameAsList)
    if vtkName in NEUROLEX_DICTIONARY:
        return vtkName
    estimate = ""
    estimateSimilarity = 0.0
    for neurolexName in NEUROLEX_DICTIONARY.keys():
        neurolexNameList = neurolexName.split(" ")
        totalSimilarity = 0
        for namePart in nameAsList:
            if namePart in neurolexNameList:
                totalSimilarity += 1
        similarity = totalSimilarity / len(nameAsList)
        if(similarity > MIN_SIMILARITY) and (similarity > estimateSimilarity):
            estimate = neurolexName
            estimateSimilarity = similarity
    return estimate

#creates a json file with the given information
def createJson(name, synonyms, vtkFileName, containers, subComponents):
    toWrite = {
        "name"          : name,
        "synonyms"      : synonyms,
        "vtkFileName"   : vtkFileName,
        "containers"    : containers,
        "subComponents" : subComponents
    }
    stringToWrite = json.dumps(toWrite, indent = 4)
    f = open(JSON_PATH + "/" + "brainParts.json", "a")# "a" for append mode
    f.write(stringToWrite)


vtkModels = getVtkModelsList(VTK_MODELS_FOLDER_PATH)
for model in vtkModels:
    name = estimateNeurolexName(model)
    if name == "":
        continue
    line = NEUROLEX_DICTIONARY[name]
    synonyms = RAW_NEUROLEX_LIST[line + 3].replace("\t3.  synonyms : ", "").split(", ")
    if synonyms[0] == "na":
        synonyms = ""
    containers = RAW_NEUROLEX_LIST[line + 9].replace("\t9.  super category : ", "").split(", ")
    if containers[0] == "na":
        containers = ""
    subComponents = RAW_NEUROLEX_LIST[line + 11].replace("\t11. has part of : ", "").split(", ")
    if subComponents[0] == "na":
        subComponents = ""
    createJson(name, synonyms, model, containers, subComponents)
