from __future__ import print_function
import cPickle as pickle
import os
import csv

__author__ = 'galaxy'
#This script was written by Philip Weiss and Megan Shortridge.
#A special thanks to Phil for the help.

mydir = os.getcwd()
li = pickle.load( open( "li.p", "rb" ))
filelist = []

for files in os.listdir(mydir):
	if files.endswith("headeradded.csv"):
		filelist.append(files)


for files in filelist:
	print(files)
	readobj = open(files, 'r')
	reader = csv.reader(readobj, "excel") #csv reader of the file

	gi_list = [] #initialize a list of GI numbers
	taxonomicranks = ["superkingdom", "kingdom", "phylum", "subphylum", "superclass", "class", "subclass", "infraclass", "superorder", "order", "infraorder", "suborder", "superfamily", "family", "subfamily", "tribe", "genus", "species"]


	GI_field = ""

	for row in reader:
		if "qseqid" in row: #then this is the header line
			for x in range (0, len(row)):
				if row[x]=="gi" or row[x]=="GI":
					GI_field = int(x) #then the column containing GI numbers is this one.
		elif "qseqid" not in row: #then it is not a headerline
			gi_list.append(row[GI_field])

	readobj.close()

	readobj = open(files, 'r')
	reader = csv.reader(readobj, "excel") #csv reader of the file
	newfilename = files.replace(".csv", "_taxonomy.csv")
	writeobj = open(newfilename, 'w', newline='')
	writer = csv.writer(writeobj, "excel")

	rownum = 0
	for row in reader:
		if row[0] != "qseqid": #this is only if this is not a header containing line
			try:
				if row[0] != "":
					tax=[]
					gi = int(gi_list[rownum])
					rownum+=1
					#print("Loading GI database")
					for x in range(len(li)):
						if gi >= li[x][0] and  gi <= li[x][1]:

							fn = "gi_" + str(li[x][0]) + "_" + str(li[x][1]) +   ".p"
							gi_to_taxon = pickle.load(open(fn, "rb"))
							tax.append(gi_to_taxon[gi])

					c=0

					#print("Obtaining Taxonomy Structure")

					rank = []
					while tax[c] != 1:

						for line in open("nodes.dmp", "rU"):
							ln = line.lstrip().split()
							if tax[c] == int(ln[0]):
								tax.append(int(ln[2]))
								if ln[4] == 'no':
									tmp = 'N/A'
								else:
									tmp = ln[4]
								rank.append(tmp)
								c+=1
							elif tax[c] < int(ln[0]):
								break

					#print("Converting nodes to names")

					name= []
					for x in range(len(tax)-1):
						if x == 0:
							offset = 3
						else:
							offset = 2
						for line in open("names.dmp", "rU"):
							ln = line.lstrip().split()
							if tax[x] == int(ln[0]):
								name.append(ln[offset])
								#print(ln[offset])
								break
					for x in range (0, len(taxonomicranks)):
						rank_type = taxonomicranks[x]
						#print(rank_type)
						rank_found = False #initialize True-False sequence
						for x in range(0, len(rank)):
							rank_name = rank[x]
							name_value = name[x]
							if rank_name == rank_type:
								rank_found = True
								row.append(name_value)

						if rank_found==False:
								row.append("N/A")
						elif rank_found ==True:
							#print("rank found")
							pass
				writer.writerow(row)
			except IndexError:
				print("Oops")
		elif row[0]=="qseqid": #this will write the header line when it first finds it.
			for x in range (0, len(taxonomicranks)):
				row.append(taxonomicranks[x])
			writer.writerow(row)

	writeobj.close()
	readobj.close()
