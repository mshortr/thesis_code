__author__ = 'galaxy'
#This one should give you your final csv files that you can do the final summarize taxonomy on.

#This will remove specified contaminant sequences from your summary file e.g. Homo sapiens.
import os
import csv

dir = ""
addon= "" #
dir = str(dir)+str(addon)
os.chdir(dir)

filelist=[]

for file in os.listdir(dir):
    if file.endswith(".csv"):
        filelist.append(file)

eliminate_list = [] #a list of contaminants to remove from file datasets, specify scientific name.
for file in filelist:
    readobj = open(file, "read")
    reader = csv.reader(readobj, "excel")
    newfn = file.replace(".csv", "_fixed.csv")
    writeobj = open(newfn, "write")
    writer = csv.writer(writeobj, "excel")
    for row in reader:
        eliminate = False
        if row[0]=="qseqid":
            pass
            writer.writerow(row)
        elif row[0]!= "qseqid":
            for x in range(0, len(eliminate_list)):
                if str(eliminate_list[x]) != str(row[44]):
                    pass
                elif str(eliminate_list[x]) == str(row[44]):
                    eliminate = True
                    print(eliminate_list[x])
            if eliminate == False:
                pass
                writer.writerow(row)
            elif eliminate == True: #then you do not write the sequence to the file
                print("something was eliminated.")
    readobj.close()
    writeobj.close()