# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile

import numpy as np

datafile = "../datasets/2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

def parse_file_instructor(datafile): # Instructor Code
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = {}
    # process all rows that contain station data
    for n in range (1, 9):
        station = sheet.cell_value(0, n)
        cv = sheet.col_values(n, start_rowx=1, end_rowx=None)

        maxval = max(cv)
        maxpos = cv.index(maxval) + 1
        maxtime = sheet.cell_value(maxpos, 0)
        realtime = xlrd.xldate_as_tuple(maxtime, 0)
        data[station] = {"maxval": maxval,
                         "maxtime": realtime}

    print data
    return data

def save_file_instructor(data, filename): # Instructor Code
    with open(filename, "w") as f:
        w = csv.writer(f, delimiter='|')
        w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
        for s in data:
            year, month, day, hour, _ , _= data[s]["maxtime"]
            w.writerow([s, year, month, day, hour, data[s]["maxval"]])

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    dates = np.array(sheet.col_values(0)[1:])
    
    for col in range(1, sheet.ncols - 1):
        station = sheet.cell_value(0, col)
        col_array = np.array(sheet.col_values(col)[1:])
        col_max_idx = col_array.argmax()
        col_max = col_array[col_max_idx]
        max_time = xlrd.xldate_as_tuple(dates[col_max_idx], 0)
        
        col_summary = [station, max_time[0], max_time[1], max_time[2], max_time[3], col_max]
        data.append(col_summary)
        
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    header = ['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']
    with open(filename, 'wb') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(header)        
        writer.writerows(data)
    
def test():
    #open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
