#This is the script that I am going to use to generate summarize taxonomy files.

import os
import csv

#maybe make one output an excel file and one output a text file with tabs that can be copied and pasted?

dir = ""
#species_list = ["Pimephales notatus", "Notropis atherinoides", "Morone chrysops", "Morone americana", "Carassius auretus", "Dorosoma cepedianum", "Ictiobus cyprinellus", "Cyprinus carpio", "Moxostoma spp", "Ictalurus punctatus", "Carpiodes cyprinus", "Aplodinotus grunniens"]
# species_list = []
# species_list.append("Pimephales notatus")
# for species in species_list:
#     dir = "/home/galaxy/Desktop/Megan Shortridge Thesis Files/datasets/final_files_greater_than_95_percent/fixed/Edited_CSV_Files/"
#     dir = dir + str(species)
species = "" # species name here
identifier_name = species #this is an identifier that you will use to designate what you want to refer to the resulting file as
os.chdir(dir)
filelist=[]
for file in os.listdir(dir):
    if file.endswith(".csv"):
        filelist.append(file)

fn = identifier_name+"_summary.csv"
writeobj = open(fn, "write")
writer = csv.writer(writeobj, "excel") #This is the output file that you will write the summary to.

fn2 = identifier_name+"_summary.txt"
writeobj2 = open(fn2, "write") # I have yet to develop this part of the script. So far it is just opening up a blank text file. May not end up doing anything with it so should delete it.

header = ["Taxon value", "Rank Type", "Per instance, seq count", "Total # unique seqs (collapsed)", "Frequency sum of all sequences","Files with taxon", "Num files w/ taxon", "Percent ID"]
writer.writerow(header)
rankdictionary=dict() #make a dictionary of ranks, 1 is the highest level, and 18 is the lowest taxonomic rank (most specific rank).
#NOTE: This specific dictionary is not currently being used but may be used later in the script if the need arises. Keep this for now.
rankdictionary['superkingdom'] = 1
rankdictionary['kingdom'] = 2
rankdictionary['phylum'] = 3
rankdictionary['subphylum'] = 4
rankdictionary['superclass'] = 5
rankdictionary['class'] = 6
rankdictionary['subclass'] = 7
rankdictionary['infraclass'] = 8
rankdictionary['superorder'] = 9
rankdictionary['order'] = 10
rankdictionary['infraorder'] = 11
rankdictionary['suborder'] = 12
rankdictionary['superfamily'] = 13
rankdictionary['family'] = 14
rankdictionary['subfamily'] = 15
rankdictionary['tribe'] = 16
rankdictionary['genus'] = 17
rankdictionary['species'] = 18
rankdictionary['Scientific name']=19

coldict=dict() #This dictionary contains the column numbers associated with any taxonomic rank for quick reference.
coldict['superkingdom'] = 26
coldict['kingdom'] = 27
coldict['phylum'] = 28
coldict['subphylum'] = 29
coldict['superclass'] = 30
coldict['class'] = 31
coldict['subclass'] = 32
coldict['infraclass'] = 33
coldict['superorder'] = 34
coldict['order'] = 35
coldict['infraorder'] = 36
coldict['suborder'] = 37
coldict['superfamily'] = 38
coldict['family'] = 39
coldict['subfamily'] = 40
coldict['tribe'] = 41
coldict['genus'] = 42
coldict['species'] = 43
coldict['Scientific name'] = 44

count_col = 46
coldict_reversed = dict([[a,b,] for b,a in coldict.items()])
#inverted_dict = dict([[v,k] for k,v in mydict.items()])

taxdict = dict() #this is a dictionary that will contain taxonomic ids present in the files.

count_dict = dict() #this is where I will have all of the counts present. How many times a particular taxon was represented in the dataset (how many unique sequences).

file_dict = dict() #this dictionary will contain the total number of files (individuals) having a certain taxonomic rank present.

percentid_dict = dict () #dictionary will contain percent identity values for that particular OTU
for file in filelist:
    print(file)
    readobj = open(file, "read")
    reader = csv.reader(readobj, "excel")
    rownumber = 0
    for row in reader:
        if row[0]!= "":
            test = row #can remove this later
            rownumber +=1
            if row[0]=="qseqid":
                header = row
                pass
            elif row[0]!="qseqid":#then it is now a header row. Continue.
                for x in range(26,45): #this is the span of the taxonomic ranks
                    ranktype = coldict_reversed[x] #This will give you the type of taxonomic rank
                    rankvalue = str(row[x]) #this will give you the rank value
                    if rankvalue in taxdict.keys():
                        if str(count_dict[rankvalue]).endswith(";") == False:
                            old_value = count_dict[rankvalue]
                            new_value = old_value+";"+str(row[46])
                            count_dict[rankvalue] = new_value
                            percentid = str(row[2])
                            old_value2 = percentid_dict[rankvalue]
                            new_value2 = old_value2 + ";"+percentid
                            percentid_dict[rankvalue]=new_value2
                        elif str(count_dict[rankvalue]).endswith(";")==True:
                            old_value = count_dict[rankvalue]
                            new_value = old_value+str(row[46]) #this will avoid the double ; error that happens.
                            count_dict[rankvalue] = new_value
                            old_value2 = percentid_dict[rankvalue]
                            new_value2 = old_value2 + str(row[2])
                            percentid_dict[rankvalue] = new_value2
                    elif rankvalue not in taxdict.keys():
                        taxdict[rankvalue] = ranktype
                        count_dict[rankvalue] = str(row[46])+";"
                        percentid_dict[rankvalue] = str(row[2])+";"
                    if rankvalue in file_dict:
                        oldstring = file_dict[rankvalue]
                        if oldstring.find(file) == -1: #this would mean that it did not find the file already attributed in there.
                            if oldstring.endswith(";")==True:
                                newstring = oldstring+str(file)
                            elif oldstring.endswith(";")==False:
                                newstring = oldstring+";"+str(file)
                            file_dict[rankvalue] = newstring
                        elif oldstring.find(file) != -1:
                            pass #if the file has already been accounted for, ignore it, and do not add to the list. That way you are only getting unique files.
                    elif rankvalue not in file_dict:
                        file_dict[rankvalue]=str(file)+";"



#once it has gone through all the files in the list, time to write excel outputfile. This would be the unique file seqs i think...double check.
total_count_dict = dict()
total_count_frequency_dict = dict() #this is all of the sequences and their frequency across the file. So this would take into account number of copies.
for key in count_dict:
    name = key
    count_summary = str(count_dict[key])
    count_delim = count_summary.split(";")


    try:
        count_delim.remove("")
    except ValueError:
        pass

    count_num = len(count_delim)

    total_count_dict[name] = count_num
    frequency_sum = 0 #this is the number of sequences total found for a particular taxonomic level.
    for x in range(0, len(count_delim)):
        count = int(count_delim[x])
        frequency_sum+=count
    total_count_frequency_dict[key] = frequency_sum



for key in taxdict:
    line=[]
    ranktype = taxdict[key]
    line.append(key)
    line.append(ranktype)
    count_summary = count_dict[key]
    line.append(count_summary)
    count_num = total_count_dict[key]
    line.append(count_num)
    frequency_sum = total_count_frequency_dict[key]
    line.append(frequency_sum)
    file_with_taxon = file_dict[key]
    line.append(file_with_taxon)
    split_number_files = file_with_taxon.split(";")
    try:
        split_number_files.remove("")
    except Exception:
        pass
    number_files = len(split_number_files)
    line.append(number_files)
    percentid_list = percentid_dict[key]
    line.append(percentid_list)
    writer.writerow(line)




writeobj.close()

