from operator import itemgetter
import datetime
import sys

'''
get_file_template

Description:
A function to return the Data Structures that holds the column names and the respective place in the file
'''
def get_file_template():
	ds = {
		"DEALERID" : 0,
		"ROCLOSEDATE" : 2,
		"STATE" : 6,
		"MILEAGE" : 10,
		"TECHNICIANS" : 11,
		"OPERATIONS" : 12,

		"TIME" : 20,

		"PARTSAMOUNT" : 14,
		"LABORAMOUNT" : 15,

		"ROTOTAL" : 17,

		"CUST_LABOR_AMT" : 23,
		"CUST_PARTS_AMT" : 24,
		"CUST_MISC_AMT" : 25,
		"WARRANTY_LABOR_AMT" : 26,
		"WARRANTY_PARTS_AMT" : 27,
		"WARRANTY_MISC_AMT" : 28,
		"INTERNAL_LABOR_AMT" : 29,
		"INTERNAL_PARTS_AMT" : 30,
		"INTERNAL_MISC_AMT" : 31,

		"YEAR" : 32,
		"MAKE" : 33,
		"MODEL" : 34

	}

	return ds

'''
avg_time_per_value

Description:
A generic function to find the time that is spent on any given key (column name). 
For eg: When the key is 'TECHNICIANS' the function calculates the time taken
per TECHNICIAN

Parameters:
filename: Name of the of file to be processed
key: Field from the file 
'''
def avg_time_per_value(filename, key):
	global result_hash

	dealers = {}
	file_pos = get_file_template()

	filehandle = open(filename)
	count = 1

	header = filehandle.readline()

	while 1:

		line = filehandle.readline()

		if not line:
			break

		data = line.split("\t")
		
		dealerid = int(data[file_pos["DEALERID"]].strip())
		
		values = len(data[file_pos[key]].split("^"))

		times = data[file_pos["TIME"]].split("^")
		totaltime = 0.0
		for time in times:
			if not time:
				continue

			atime = float(time)

			totaltime += atime

		if dealerid in dealers:
			dealers[dealerid][key] += values
			dealers[dealerid]["TIME"] += totaltime
		else:
			dealers[dealerid] = {}
			dealers[dealerid][key] = values
			dealers[dealerid]["TIME"] = totaltime

	filehandle.close()
	
	averagetime = {}

	for dealer in dealers:
		averagetime[dealer] = float((dealers[dealer]["TIME"] * 60)/dealers[dealer][key])

	sorteddict = dict(sorted(averagetime.iteritems(), key=itemgetter(1), reverse=False)[:10])

	for dealerid in sorteddict.keys():
		if not dealerid in result_hash:
			result_hash[dealerid] = 1
		else:
			result_hash[dealerid] += 1


	for key in sorteddict:
		print key, " ", sorteddict[key]

	print

'''
per_customer

Description:
A generic function to find the unique values of any given key (column name) 
For eg: When the key 'LABORAMOUNT, INTERNAL_MISC_AMT etc' are passed, the function calculates the sum of these
cost per customer

Parameters:
filename: Name of the of file to be processed
key: Field from the file 
'''
def unique_values(filename, key):
	dealers = {}
	file_pos = get_file_template()
	global result_hash
	filehandle = open(filename)
	count = 1

	header = filehandle.readline()

	while 1:

		line = filehandle.readline()

		if not line:
			break

		data = line.split("\t")
		
		dealerid = int(data[file_pos["DEALERID"]].strip())

		values = data[file_pos[key]].split("^")

		if dealerid in dealers:
			for value in values:
				if not value in dealers[dealerid]:
					dealers[dealerid].append(value)
		else:
			dealers[dealerid] = values

	filehandle.close()

	operationscount = {}
	for dealer in dealers:
		operationscount[dealer] = len(dealers[dealer])

	sorteddict = dict(sorted(operationscount.iteritems(), key=itemgetter(1), reverse=True)[:10])

	result = []
	result = sorteddict.keys()

	for dealerid in result:
		
		if not dealerid in result_hash:
			result_hash[dealerid] = 1
		else:
			result_hash[dealerid] += 1

	
	for key in sorteddict:
		print key, " ", sorteddict[key]

	print

'''
per_customer

Description:
A generic function to find the values of the passed key (column name) per customer
For eg: When the key is 'TECHNICIANS' the function calculates how many unique TECHNICIANS
a dealer has

Parameters:
filename: Name of the of file to be processed
key: Field from the file 
'''
def per_customer(filename, keys, valuecounter = 0):
	dealers = {}
	file_pos = get_file_template()
	global result_hash
	filehandle = open(filename)
	count = 1

	header = filehandle.readline()

	while 1:

		line = filehandle.readline()

		if not line:
			break

		data = line.split("\t")
		
		dealerid = int(data[file_pos["DEALERID"]].strip())

		totalvalue = 0.0
		for key in keys:
			values = data[file_pos[key]].split("^")

			for value in values:
				if not value:
					continue
				if valuecounter == 1:
					totalvalue += 1
				else:
					totalvalue += float(value)

		if dealerid in dealers:
			dealers[dealerid]["VALUE"] += totalvalue
			dealers[dealerid]["COUNT"] += 1.0

		else:
			dealers[dealerid] = {}
			dealers[dealerid]["VALUE"] = totalvalue
			dealers[dealerid]["COUNT"] = 1.0

	filehandle.close()

	avg_values = {}

	for dealerid in dealers:
		avg_values[dealerid] = float (dealers[dealerid]["VALUE"] / dealers[dealerid]["COUNT"])

	sorteddict = dict(sorted(avg_values.iteritems(), key=itemgetter(1), reverse=False)[:10])

	sorted_x = sorted(sorteddict.items(), key=itemgetter(1))

	result = []
	for value in sorted_x[::-1]:
		result.append(value[0])
		print value[0], " ", value[1]

	for dealerid in result:
		
		if not dealerid in result_hash:
			result_hash[dealerid] = 1
		else:
			result_hash[dealerid] += 1

	print

'''
count 

Description:
A helper function that would count the number of occurances of a specific Key 
'''
def count(filename, key, addtoresult = 0, isinteger = 0):
	dealers = {}
	filehandle = open(filename)
	global result_hash
	fileds = get_file_template()

	header = filehandle.readline()
	values = {}

	while 1:
		line = filehandle.readline()
		
		if not line:
			break

		data = line.split("\t")
		value = data[fileds[key]].strip()

		if not value:
			continue

		if isinteger:
			value = int(data[fileds[key]].strip())
		else:
			value = data[fileds[key]].strip()

		if value in values:
			values[value] += 1
		else:
			values[value] = 1

	filehandle.close()

	# sorting the result based on the values and extracting only the top 10
	sorteddict = dict(sorted(values.iteritems(), key=itemgetter(1), reverse=True)[:10])

	if addtoresult:
		for key in sorteddict.keys():
			
			if not key in result_hash:
				result_hash[key] = 1
			else:
				result_hash[key] += 1

	for key in sorteddict:
		print key," ", sorteddict[key]

	print

'''
datetime_processing

Description:
A function to calculate the number of repairs that are closed on every month
'''
def datetime_processing(filename):
	values = {}
	filehandle = open(filename)
	ds = get_file_template()
	header = filehandle.readline()

	while 1:
		line = filehandle.readline()

		if not line:
			break

		data = line.split("\t")
		date = data[ds["ROCLOSEDATE"]].strip()
		#print date
		dt = datetime.datetime.strptime(date, '%m/%d/%Y')

		if dt.year in values:
			if dt.month in values[dt.year]:
				values[dt.year][dt.month] += 1
			else:
				values[dt.year][dt.month] = 1
		else:
			values[dt.year] = {}
			values[dt.year][dt.month] = 1

	filehandle.close()

	monthcount = 0.0
	value = 0.0
	for year in sorted(values.keys()):
		months = values[year]
		monthcount = len(months)
		for month in sorted(months.keys()):
			
			value += values[year][month]
		print "Year ", year, " Avg ", float(value/monthcount)

		monthcount, value = 0.0, 0.0

	print 

'''
effectivecar

Description:
A function to calculate the most and least effective car based on the mileage
'''
def effectivecar(filename):
	values = {}
	filehandle = open(filename)

	fileds = get_file_template()

	header = filehandle.readline()
	values = {}

	while 1:
		line = filehandle.readline()
		
		if not line:
			break

		data = line.split("\t")
		make = data[fileds["MAKE"]].strip()
		car = data[fileds["MODEL"]].strip()

		mileage = data[fileds["MILEAGE"]].strip()

		if not mileage or not car or not make:
			continue
		else:
			mileage = int(mileage)

		if mileage < 10000:
			continue

		if make in values:
			if car in values[make]:
				values[make][car]["MILEAGE"] += mileage
				values[make][car]["COUNT"] += 1
			else:
				values[make][car] = {}
				values[make][car]["MILEAGE"] = mileage
				values[make][car]["COUNT"] = 1
		else:
			values[make] = {}
			values[make][car] = {}
			values[make][car]["MILEAGE"] = mileage
			values[make][car]["COUNT"] = 1

	filehandle.close()

	minvalues = {}

	print "Printing MAKE, Least Reliable Car, Mileage"
	for make in sorted(values.keys()):
		minvalues[make] = {}
		minmodelname, minmodelvalue = "x", sys.maxint
		for car in values[make]:
			val = values[make][car]["MILEAGE"]/values[make][car]["COUNT"]
			if val < minmodelvalue:
				minmodelvalue = val
				minmodelname = car

		print make," ",minmodelname," ",minmodelvalue
		minvalues[make][minmodelname] = minmodelvalue

	minval = sys.maxint
	mincarname = ""

	maxval = -1 * sys.maxint
	maxcarname = ""

	for make in minvalues:
		for car in minvalues[make]:
			if minvalues[make][car] < minval:
				minval = minvalues[make][car]
				mincarname = car

			if minvalues[make][car] > maxval:
				maxval = minvalues[make][car]
				maxcarname = car

	print
	print "Least Reliable Car ", mincarname, minval
	print "Most Reliable Car", maxcarname, maxval

	print 

'''
yearanalysis

Description:
A function to generate the report that showcases the car, year made, number of times it has been brought in for repair
'''
def yearanalysis(filename):
	dealers = {}
	filehandle = open(filename)

	fileds = get_file_template()

	header = filehandle.readline()
	values = {}

	while 1:
		line = filehandle.readline()
		
		if not line:
			break

		data = line.split("\t")
		year = data[fileds["YEAR"]].strip()
		car = data[fileds["MODEL"]].strip()

		if not year or not car:
			continue
		else:
			year = int(year)

		if car in values:
			if year in values[car]:
				values[car][year] += 1
			else:
				values[car][year] = 1
		else:
			values[car] = {}
			values[car][year] = 1


	filehandle.close()

	#Commenting the Print Since this would generate lot of data
	#Uncomment and run the script to display that in the output
	# for car in sorted(values.keys()):
	# 	for year in values[car]:
	# 		print car, year, values[car][year]

	print


if __name__ == '__main__':
	# a global hash to store the dealers matched in various criterias
	result_hash = {}

	print "Report of car, year made, number of repairs"
	yearanalysis("RO_Example.txt")
	print "Output of the report is commented since it would print lot of data, please uncomment it to print the data"

	print "Most and Least reliable car"
	effectivecar("RO_Example.txt")

	print "Number of repairs recorded month/year"
	datetime_processing("RO_Example.txt")

	print "Number of repairs with respect to a particular year"
	count("RO_Example.txt", "YEAR", 0, 1)

	print "Number of repairs with respect to a particular car make"
	count("RO_Example.txt", "MAKE")

	print "Number of repairs with respect to a particular car model"
	count("RO_Example.txt", "MODEL")

	print "Dealers who have handled most cases"
	count("RO_Example.txt", "DEALERID", 1, 1)

	print "Dealers who have less average time per technicians/operations"
	avg_time_per_value("RO_Example.txt", "TECHNICIANS")

	print "Dealers who have more unique operations"
	unique_values("RO_Example.txt", "OPERATIONS")

	print "Dealers who have more unique technicians"
	unique_values("RO_Example.txt", "TECHNICIANS")

	print "Dealers who have less cost per customer"
	per_customer("RO_Example.txt", ["PARTSAMOUNT","LABORAMOUNT","ROTOTAL","CUST_LABOR_AMT","CUST_PARTS_AMT","CUST_MISC_AMT","WARRANTY_LABOR_AMT","WARRANTY_PARTS_AMT","WARRANTY_MISC_AMT","INTERNAL_LABOR_AMT","INTERNAL_PARTS_AMT","INTERNAL_MISC_AMT"])

	print "Technicians per customer"
	per_customer("RO_Example.txt", ["TECHNICIANS"], 1)

	#Processing and fetching only those dealers who have matched in atleast 2 out of 6 criterias defined for the effective dealers
	print "Most effective Dealers"
	for dealer in result_hash:
		if result_hash[dealer] >= 2:
			print dealer, result_hash[dealer]