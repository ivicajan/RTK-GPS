from pyubx2 import UBXReader
import csv

# This program is used to process the log file that produced in MainProgram
# Expected Output: rtk data file and gps data file

roundName='13'
f1 = open('./data/rtkOutput'+roundName+'.csv', 'w',newline = '') # stands for gps data file
f2 = open('./data/gpsOutput'+roundName+'.csv', 'w',newline = '') # stands for rtk data file
# Previous order was reversed because I mistoke the odd line to be correct data and even line to be raw data
# as they proposed in specification, while it actually not, but I'm not changing that naming for files.


writer1 = csv.writer(f1)
writer1.writerow(['lat','lng'])
writer2 = csv.writer(f2)
writer2.writerow(['lat','lng'])
stream = open('./data/oriLog'+roundName+'.txt', 'rb')
ubr = UBXReader(stream, protfilter=2)
for (raw_data, parsed_data) in ubr: 
    print(parsed_data)
    lat=parsed_data.lat
    lng=parsed_data.lon
    if parsed_data.identity=='NAV2-PVT':
        writer1.writerow([lat,lng])
    else:
        writer2.writerow([lat,lng])