__author__ = 'galaxy'
#use this to filter out reads with less than 95% match with subject sequence.
import os
import csv

dir = ""
addon= "" #if species specific directories, you can add the species here as a shortcut.
dir = str(dir)+str(addon)
os.chdir(dir)

filelist=[]
for file in os.listdir(dir):
        filelist.append(file)

count = 0
for file in filelist:
    readobj = open(file, "read")
    reader = csv.reader(readobj, "excel")
    newfn = file.replace(".csv", "_fixed.csv")
    writeobj = open(newfn, "write")
    writer = csv.writer(writeobj, "excel")
    num_rows = 0
    for row in reader:
        if row[0]=="qseqid":
            writer.writerow(row)
            num_rows += 1
        elif row[0]!= "qseqid":
            num_rows += 1
            percentid = float(row[2])
            if percentid>=95.00:
                writer.writerow(row)
            elif percentid<95.00:
                count += 1

    readobj.close()
    writeobj.close()