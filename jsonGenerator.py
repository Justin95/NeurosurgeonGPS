"""
    This script converts files from the old neurolex format to a new json based format.
    It also uses a name matching strategy to try and match the file to a vtk model, not 100% effective.
    The matching will need to be improved.

    @author Justin Bonner
"""

import json
import os.path

#the file path to the folder containing neurolex text files
NEUROLEX_FOLDER_PATH = "neurolex" #relative file path, neurolex folder is in the same folder as this script

#the file path to the folder containing vtk model files
VTK_MODELS_FOLDER_PATH = "models"#relative file path, models folder is in the same folder as this script

#the file path in which the Json will be written
JSON_PATH = ""#relative file path, put the json into the same directory this script is in

#the minimum similarity between a neurolex name and a vtk file name for identification
MIN_SIMILARITY = .75

"""
    This function reads the neurolex text files and puts each line in a list
"""
def getNeurolexList():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #neurolex text files are A.txt, B.txt etc, this is a short cut.
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

"""
    create a dictionary mapping string brain part names to the line number in which they appear in RAW_NEUROLEX_LIST
"""
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

"""
    This function returns a list of the model file names in the specified directory.
    It raises an IO Error if there is no such directory
"""
def getVtkModelsList(filePath):
    if not os.path.exists(filePath):
        raise IOError("File not found:  " + filePath)
    return os.listdir(filePath)


"""
    This function returns the estimated Neurolex name match for a given vtk file name.
    If no match satisfies MIN_SIMILARITY match requirment, then an empty string is returned.

    For future improvements try creating a dictionary with a value for each word used in
    all the neurolex and vtk names combinded, the more freqent a word in both lists the less it is worth in a match.
    ex: 'left' is a common word used so it should be worth less matching points when both a vtk file name
    and a neurolex name contain it.
"""
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
                totalSimilarity += len(namePart) / float(len(neurolexName))
        similarity = totalSimilarity / len(neurolexNameList) # or try len(nameAsList)
        if(similarity > MIN_SIMILARITY) and (similarity > estimateSimilarity):
            estimate = neurolexName
            estimateSimilarity = similarity
    return estimate

"""
    This function creates a json file with the given list of dictionaries
"""
def createJson(listOfDictionaries):
    stringToWrite = json.dumps(listOfDictionaries, indent = 4)
    f = open(JSON_PATH + "brainParts.json", "a")# "a" for append mode
    f.write(stringToWrite)
    f.close()

"""
    This function creates a dictionary out of each of its parameters
"""
def createDictionary(name, synonyms, vtkFileName, containers, subComponents):
    toWrite = {
        "name"          : name,
        "synonyms"      : synonyms,
        "vtkFileName"   : vtkFileName,
        "containers"    : containers,
        "subComponents" : subComponents
    }
    return toWrite

#utility functions are all defined, they are used to make the json here
vtkModels = getVtkModelsList(VTK_MODELS_FOLDER_PATH)
dictionaryList = list()
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
    dictionaryList.append(createDictionary(name, synonyms, model, containers, subComponents))
print(str(len(dictionaryList)) + " matches found")
createJson(dictionaryList)


