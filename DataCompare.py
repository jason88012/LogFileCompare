import glob
import re
import sys

# Define debug parameter
debug_mode = bool(0)

# save files path
#pre_datas = glob.glob('/home/ezluxja/Test/PreCheck/*.log')
#post_datas = glob.glob('/home/ezluxja/Test/PostCheck/*.log')

# Mac test file path
pre_datas = glob.glob('/Users/jason/Desktop/Test/PreCheck/*.log')
post_datas = glob.glob('/Users/jason/Desktop/Test/PostCheck/*.log')

# Test certain file's path
test_pre_path = "/home/ezluxja/Test/PreCheck/LC610003.log"
test_post_path = "/home/ezluxja/Test/PostCheck/LC610003.log"

pre_alarm_count = 0
post_alarm_count = 0

attr_name_list = []

data_length = 1
#data_length = len(pre_datas)
for site_num in range (data_length):

	# Allocate new repository to save site datas
	precheck_Cell_datas = {"Site name":[], "Cell name":[], "Cell Ad.State":[], "Cell Op.State":[]}
	precheck_RRU_datas = {"Site name":[], "RRU name":[], "RRU Ad.State":[], "RRU Op.State":[]}
	precheck_Alarm_datas = {"Site name":[], "Alarm":[]}

	postcheck_Cell_datas = {"Site name":[], "Cell name":[], "Cell Ad.State":[], "Cell Op.State":[]}
	postcheck_RRU_datas = {"Site name":[], "RRU name":[], "RRU Ad.State":[], "RRU Op.State":[]}
	postcheck_Alarm_datas = {"Site name":[], "Alarm":[]}

	# Test certain file code
	'''
	pre_file = open(test_pre_path, 'r')
	post_file = open(test_post_path, 'r')
	test_path = test_pre_path.split("/")
	enb_name = test_path[len(test_path) - 1][:-4]
	'''
	
	pre_file = open(pre_datas[site_num], 'r')
	post_file = open(post_datas[site_num], 'r')
	name_term = pre_datas[site_num].split("/")
	enb_name = name_term[len(name_term) - 1][:-4]

	#print("Checking status...")

	# Precheck...
	pre_alarm_lines = []
	for i, line in enumerate(pre_file, 1):
		# check precheck EUtranCellFDD status
		if re.search("ENodeBFunction=1,EUtranCellFDD", line):
			blocks = line.split()
			# proxy 0/1 state 0/1 state CellName
			if (len(blocks) == 6):
				if "ENodeBFunction=1,EUtranCellFDD" in blocks[5]:
					cellfdd_term = blocks[5].split("=")
					#print(cellfdd_term[len(cellfdd_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					precheck_Cell_datas["Site name"].append(enb_name)
					precheck_Cell_datas["Cell name"].append(cellfdd_term[len(cellfdd_term) - 1])
					precheck_Cell_datas["Cell Ad.State"].append(blocks[2][1:-1])
					precheck_Cell_datas["Cell Op.State"].append(blocks[4][1:-1])

		# check precheck RRU status
		if re.search("AuxPlugInUnit", line):
			blocks = line.split()
			# proxy 0/1 state 0/1 state RRUname
			if (len(blocks) == 6):
				if "AuxPlugInUnit" in blocks[5]:
					rru_term = blocks[5].split("=")
					#print(rru_term[len(rru_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					precheck_RRU_datas["Site name"].append(enb_name)
					precheck_RRU_datas["RRU name"].append(rru_term[len(rru_term) - 1])
					precheck_RRU_datas["RRU Ad.State"].append(blocks[2][1:-1])
					precheck_RRU_datas["RRU Op.State"].append(blocks[4][1:-1])

		# check precheck alarm:
		if re.search("Nr of active alarms", line):
			blocks = line.split()
			alarms_num = int(blocks[len(blocks) - 1])
			if (alarms_num != 0):
				for count in range(alarms_num):
					pre_alarm_lines.append(i+count+4)
			else:
				precheck_Alarm_datas["Site name"].append(enb_name)
				precheck_Alarm_datas["Alarm"].append("NULL")
		if i in pre_alarm_lines:
			#print(line)
			pre_alarm_count += 1
			precheck_Alarm_datas["Site name"].append(enb_name)
			precheck_Alarm_datas["Alarm"].append(line)

	# Close precheck file
	pre_file.close()

	# Postcheck...		
	post_alarm_lines = []
	post_check_mo = []
	post_check_attr = []
	for i, line in enumerate(post_file, 1):
		# check postcheck EUtranCellFDD status
		if re.search("ENodeBFunction=1,EUtranCellFDD", line):
			blocks = line.split()
			if (len(blocks) == 6):
				if "ENodeBFunction=1,EUtranCellFDD" in blocks[5]:
					cellfdd_term = blocks[5].split("=")
					#print(cellfdd_term[len(cellfdd_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					postcheck_Cell_datas["Site name"].append(enb_name)
					postcheck_Cell_datas["Cell name"].append(cellfdd_term[len(cellfdd_term) - 1])
					postcheck_Cell_datas["Cell Ad.State"].append(blocks[2][1:-1])
					postcheck_Cell_datas["Cell Op.State"].append(blocks[4][1:-1])

		# check postcheck RRU status	
		if re.search("AuxPlugInUnit", line):
			blocks = line.split()
			if (len(blocks) == 6):
				if "AuxPlugInUnit" in blocks[5]:
					rru_term = blocks[5].split("=")
					#print(rru_term[len(rru_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					postcheck_RRU_datas["Site name"].append(enb_name)
					postcheck_RRU_datas["RRU name"].append(rru_term[len(rru_term) - 1])
					postcheck_RRU_datas["RRU Ad.State"].append(blocks[2][1:-1])
					postcheck_RRU_datas["RRU Op.State"].append(blocks[4][1:-1])

		# check postcheck alarm:
		if re.search("Nr of active alarms", line):
			blocks = line.split()
			alarms_num = int(blocks[len(blocks) - 1])
			if (alarms_num != 0):
				for count in range(alarms_num):
					post_alarm_lines.append(i+count+4)
			else:
				postcheck_Alarm_datas["Site name"].append(enb_name)
				postcheck_Alarm_datas["Alarm"].append("NULL")
		if i in post_alarm_lines:
			#print(line)
			post_alarm_count += 1
			postcheck_Alarm_datas["Site name"].append(enb_name)
			postcheck_Alarm_datas["Alarm"].append(line)

		# List desire checking MOs and attributes:
		if re.search("get", line):
			blocks = line.split()
			#print(blocks)
			if (enb_name in blocks[0]):
				# if len == 3: enb_name> get MO
				if (len(blocks) == 3):
					post_check_mo.append(blocks[len(blocks) - 1])
				# if len == 4: enb_name> get MO attribute
				elif (len(blocks) >= 4):
					post_check_attr.append(blocks[len(blocks) - 1])

	if debug_mode == 1:
		# Check Cell, RRU, Alarm compares
		print(precheck_Cell_datas)
		print(precheck_RRU_datas)
		print(precheck_Alarm_datas)

		print(postcheck_Cell_datas)
		print(postcheck_RRU_datas)
		print(postcheck_Alarm_datas)

		# Check what MOs and attributes should find
		print("post_check_mo:")
		print(post_check_mo)
		print("post_check_attr:")
		print(post_check_attr)

		# Check total alarms
		print ("precheck total alarm:", pre_alarm_count)
		print ("postcheck total alarm:", post_alarm_count)

	# Preprocess the MO's searching targets 
	post_check_mo_find = []
	for i in range(len(post_check_mo)):
		blocks = post_check_mo[i].split(",")
		post_check_mo_find.append(blocks[len(blocks) - 1])

	# Reset the file reader pointer
	post_file.seek(0)

	# Indicate which MOs and attribute is been searched
	attr = 0
	mo = 0

	# Indicate how many MOs and attributes should be found
	count = 0
	attr_num = 0
	mo_num = 0

	# Indicate how many struct and elements should be found
	struct_num = 0
	element_num = 0

	# Searching flags
	attr_detect = bool(0)
	mo_detect = bool(0)
	mo_record = bool(0)
	mo_struct_detect = bool(0)
	mo_element_detect = bool(0)

	# Set an empty string for saving attribute name
	attr_name = None
	struct_id = None
	struct_name = None

	attr_result = {"Site name":[], "MO's name":[], "Attribute":[], "Value":[]}
	mo_result = []

	for i, line in enumerate(post_file, 1):

		#===============================================================================#
		# 					Indicate how to find desire attributes						#
		#===============================================================================#

		# Find first attribute, which is in get command line
		if re.search(post_check_attr[attr], line):
			attr_term = line.split()
			if (len(attr_term) == 3):
				count += 1
				attr_detect = 1
				blocks = line.split()
				attr_result["Site name"].append(enb_name)
				attr_result["MO's name"].append(blocks[0])
				attr_result["Attribute"].append(blocks[1])
				attr_result["Value"].append(blocks[2])
				#print(blocks)

		# Find how many MOs has this attributes
		if re.search("Total:", line) and attr_detect == 1:
			total_term = line.split()
			attr_num = int(total_term[1])
			# Total: n MOs

		# Already find all attributes, reset all require counter and flags
		if (count == attr_num) and (attr_detect == 1):
			count = 0
			attr_num = 0
			attr_detect = 0
			if (attr != len(post_check_attr) - 1):
				attr += 1

		#===============================================================================#
		# 						Indicate how to find desire MOs							#
		#===============================================================================#
		
		# Find first MO, which is in get command line
		if re.search(post_check_mo_find[mo], line):
			mo_term = line.split()
			if (len(mo_term) == 2):
				count += 1
				mo_detect = 1

		# If already detect MO, record it from '=' until find another '='
		if re.search("=====", line) and mo_detect == 1 and mo_record == 0:
			mo_record = 1
		elif re.search("=====", line) and mo_detect == 1 and mo_record == 1:
			mo_record = 0
		# Record attriutes data in MOs
		elif mo_record == 1:
			blocks = line.split()
			# Struct detected by keyword "t[num] ="
			if (blocks[len(blocks) - 1] == "="):
				struct_num = int(blocks[1][2:-1])
				struct_name = blocks[0]
				attr_name = blocks[0]
				# attr_value = str(struct_num) + " members"

			# Struct detected by keyword "Struct{num}"
			elif re.search("Struct", blocks[len(blocks) - 1]):
				struct_num = int(blocks[1][7:-1])
				struct_name = blocks[0]
				attr_name = blocks[0]
				# attr_value = str(struct_num) + "members"

			# Struct element statement, by keyword ">>>" 
			elif blocks[0] == ">>>":
				# This line indicate struct information
				if re.search("Struct", line) and len(blocks) > 2:
					struct_id = blocks[1]
					ele_num = int(blocks[3])
					attr_name = struct_name + struct_id
					# attr_value = ele_num
				else:
					attr_name = struct_id + blocks[1]
					for rest in range(3, len(blocks)):
						pass
						# attr_value += blocks[rest]

			# Normal attribute and values
			else:
				# There is no value in this attribute
				if (len(blocks) == 1):
					pass
					attr_name = blocks[0]
					# attr_value = None
				else:
					attr_name = blocks[0]
					for rest in range(1, len(blocks)):
						pass
						# attr_value += blocks[rest]

			if attr_name not in attr_name_list:
				attr_name_list.append(attr_name)


		# Find how many MOs should been found
		if re.search("Total:", line) and mo_detect == 1:
			total_term = line.split()
			mo_num = int(total_term[1])
			# Total: n MOs

		# Already find all MOs, reset all require counter and flags
		if (count == mo_num) and (mo_detect == 1):
			count = 0
			mo_num = 0
			mo_detect = 0
			if (mo != len(post_check_mo_find) - 1):
				mo += 1



	#print(attr_result)
print(attr_name_list)















