import glob, os, os.path, copy

def main():
	for files in os.walk('/home/zero/Desktop/obj'):
		for name in files:
			fileNameArrayOriginal =  name

	fileNameArray = copy.copy(fileNameArrayOriginal)

	for i in range(1, len(fileNameArray)):
	#for i in range(1, 2): #DEBUG
		if (fileNameArray[i].startswith("FJ")):
			fo = open('/home/zero/Desktop/obj/'+(fileNameArray[i]), "r")
			#print "Name of the file: ", fo.name #DEBUG
 			temp1 = fo.readlines(1000)
			englishName = temp1[10]
			englishName = englishName.rstrip('\n')
			fo.close()
			if englishName.startswith("# English name :"):
				englishName = englishName[17:]
				#print(englishName)	#DEBUG
				temp2 = fileNameArray[i]
				fileNameArray[i] = englishName+'_'+temp2
				#print(fileNameArray[i]) #% (i) # What happens if I comment this back in?

	out = open('/home/zero/Desktop/the_list.txt', 'w')
	for j in range(1, len(fileNameArray)):
		#print(fileNameArray[j])		#DEBUG
		#print(fileNameArrayOriginal[j])	#DEBUG
		os.rename('/home/zero/Desktop/obj/'+(fileNameArrayOriginal[j]), '/home/zero/Desktop/obj/'+(fileNameArray[j]))
		out.write(fileNameArray[j])
		out.write("\n")
	out.close()
main()