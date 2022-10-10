import json
import csv
import sys
import os

jsonfile = sys.argv[1]

csvfile = jsonfile + ".csv"

with open(jsonfile) as json_file:
    jsondata = json.load(json_file)
 
data_file = open(csvfile, 'w', newline='')
csv_writer = csv.writer(data_file)
 
line_no = 0
for data in jsondata:
    if line_no == 0:
        header = data.keys()
        csv_writer.writerow(header)
        line_no += 1
    csv_writer.writerow(data.values())
 
data_file.close()

print ("created " + csvfile)

