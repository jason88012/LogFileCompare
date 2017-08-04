import glob
import os
import re
import sys
import timeit as t
import xlsxwriter as xw

# Check input parameter
if (len(sys.argv) != 4):
	print("ERROR: Wrong input parameters")
	print("Usage: python3 DataCompare.py [Precheck folder name] [Postcheck folder name] [Output file name]")
	quit()

# Set checkfile path
cwd = os.getcwd()
cwd += "/"
pre_f_term = sys.argv[1].split("/")
post_f_term = sys.argv[2].split("/")
pre_path = cwd + pre_f_term[0] + "/*.log"
post_path = cwd + post_f_term[0] + "/*.log"

# Set time counter start
start_t = t.default_timer()

# Save files path
pre_datas = glob.glob(pre_path)
post_datas = glob.glob(post_path)

# Test certain file's path
#test_pre_path = '/home/ezluxja/Test/PreCheck/LC500023.log'
#test_post_path = '/home/ezluxja/Test/PostCheck/LC500023.log'

# Create a workbook and set font type
workbook = xw.Workbook(sys.argv[3] + '.xlsx')
arial = workbook.add_format()
arial.set_font_name('Arial')

# Create some neccesary worksheet: cell, ru, alarm, attributes
cell_sheet = workbook.add_worksheet('Cell')
pre_cell_couter = 1
post_cell_counter = 1
cell_sheet.write(0, 0, 'Site name', arial)
cell_sheet.write(0, 1, 'Cell name', arial)
cell_sheet.write(0, 2, 'pre-check', arial)
cell_sheet.write(0, 3, 'post-check', arial)
cell_sheet.write(0, 4, 'Check required', arial)

ru_sheet = workbook.add_worksheet('RU')
pre_ru_counter = 1
post_ru_counter = 1
ru_sheet.write(0, 0, 'Site name', arial)
ru_sheet.write(0, 1, 'RU name',arial)
ru_sheet.write(0, 2, 'pre-check', arial)
ru_sheet.write(0, 3, 'post-check',arial)
ru_sheet.write(0, 4, 'Check required', arial)

alarm_sheet = workbook.add_worksheet('Alarm')
pre_alarm_counter = 1
post_alarm_counter = 1
alarm_sheet.write(0, 0, 'Site name', arial)
alarm_sheet.write(0, 1, 'Alarm type', arial)
alarm_sheet.write(0, 2, 'Alarm MO', arial)
alarm_sheet.write(0, 3, 'Alarm reason', arial)
alarm_sheet.write(0, 4, 'trouble shoot required', arial)

attr_sheet = workbook.add_worksheet('Parameters')
attr_counter = 1
attr_sheet.write(0, 0, 'Site name',arial)
attr_sheet.write(0, 1, 'MO name',arial)
attr_sheet.write(0, 2, 'Attribute',arial)
attr_sheet.write(0, 3, 'Value',arial)

# Calculate alarms numbers
pre_alarm_count = 0
post_alarm_count = 0
alarm_line_count = 1
pst_line_count = 1

# Calculate longest string in these cells
l_enb_name = 0

l_cell_name = 0
l_cell_st = 0

l_ru_name = 0
l_ru_st = 0

l_al_type = 0
l_al_mo = 0
l_al_re = 0

l_mo_name = 0
l_attr_name = 0
l_value = 0

l_scanner_name = 0

# record names
mo_attr_name = []
mo_line_count = []
attr_name_list = []
post_check_mo_find = []
mo_sheet_name = []
mo_sheet_ls = []

#data_length = 1
data_length = len(pre_datas)
for site_num in range (data_length):

	# Allocate new repository to save ru and cell datas for compare
	pre_cell_st = []
	pre_ru_st = []

	# Allocate new repository to save alarm datas
	pre_alarm_datas = []
	post_alarm_datas = []
	pre_alarm_lines = []
	post_alarm_lines = []

	# Test certain file code
	#pre_file = open(test_pre_path, 'r')
	#post_file = open(test_post_path, 'r')
	#test_path = test_pre_path.split("/")
	#enb_name = test_path[len(test_path) - 1][:-4]
	
	pre_file = open(pre_datas[site_num], 'r')
	post_file = open(post_datas[site_num], 'r')
	name_term = pre_datas[site_num].split("/")
	enb_name = name_term[len(name_term) - 1][:-4]

	print("Now checking...", enb_name)

	# Precheck...
	for i, line in enumerate(pre_file, 1):
		# check precheck EUtranCellFDD status
		if re.search("ENodeBFunction=1,EUtranCellFDD", line):
			blocks = line.split()
			# proxy 0/1 state 0/1 state CellName
			if (len(blocks) == 6):
				if 'ENodeBFunction=1,EUtranCellFDD' in blocks[5]:
					cellfdd_term = blocks[5].split("=")
					#print(cellfdd_term[len(cellfdd_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					cell_sheet.write(pre_cell_couter, 0, enb_name, arial)
					cell_sheet.write(pre_cell_couter, 1, cellfdd_term[len(cellfdd_term) - 1], arial)
					cell_sheet.write(pre_cell_couter, 2, blocks[2][1:-1] + "_" + blocks[4][1:-1], arial)
					pre_cell_st.append(blocks[2][1:-1] + "_" + blocks[4][1:-1])
					pre_cell_couter += 1
					if site_num == 0:
						if (len(enb_name) > l_enb_name):
							l_enb_name = len(enb_name)
						if (len(cellfdd_term[len(cellfdd_term) - 1]) > l_cell_name):
							l_cell_name = len(cellfdd_term[len(cellfdd_term) - 1])
						if (len(blocks[2][1:-1] + "_" + blocks[4][1:-1]) > l_cell_st):
							l_cell_st = len(blocks[2][1:-1] + "_" + blocks[4][1:-1])

		# check precheck RRU status
		elif re.search('AuxPlugInUnit', line):
			blocks = line.split()
			# proxy 0/1 state 0/1 state RRUname
			if (len(blocks) == 6):
				if "AuxPlugInUnit" in blocks[5]:
					rru_term = blocks[5].split("=")
					#print(rru_term[len(rru_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					ru_sheet.write(pre_ru_counter, 0, enb_name, arial)
					ru_sheet.write(pre_ru_counter, 1, rru_term[len(rru_term) - 1], arial)
					ru_sheet.write(pre_ru_counter, 2, blocks[2][1:-1] + "_" + blocks[4][1:-1], arial)
					pre_ru_st.append(blocks[2][1:-1] + "_" + blocks[4][1:-1])
					pre_ru_counter += 1
					if site_num == 0:
						if (len(rru_term[len(cellfdd_term) - 1]) > l_ru_name):
							l_ru_name = len(rru_term[len(cellfdd_term) - 1])
						if (len(blocks[2][1:-1] + "_" + blocks[4][1:-1]) > l_ru_st):
							l_ru_st = len(blocks[2][1:-1] + "_" + blocks[4][1:-1])

		# check precheck alarm:
		elif re.search('Nr of active alarms', line):
			blocks = line.split()
			alarms_num = int(blocks[len(blocks) - 1])
			if (alarms_num != 0):
				for count in range(alarms_num):
					pre_alarm_lines.append(i+count+4)

		if i in pre_alarm_lines:
			#print(line)
			pre_alarm_count += 1
			pre_alarm_datas.append(line)

	# Close precheck file
	pre_file.close()

	# Define post-check cell state and ru state parameter
	post_cell_check_count = 0
	post_ru_check_count = 0


	# Postcheck...		
	post_check_mo = []
	post_check_attr = []
	post_check_attr_line = []
	pst_lines = None
	for i, line in enumerate(post_file, 1):
		# check postcheck EUtranCellFDD status
		if re.search('ENodeBFunction=1,EUtranCellFDD', line):
			blocks = line.split()
			if (len(blocks) == 6):
				if "ENodeBFunction=1,EUtranCellFDD" in blocks[5]:
					cellfdd_term = blocks[5].split("=")
					#print(cellfdd_term[len(cellfdd_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					cell_sheet.write(post_cell_counter, 3, blocks[2][1:-1] + "_" + blocks[4][1:-1], arial)
					if (blocks[2][1:-1] + "_" + blocks[4][1:-1] != pre_cell_st[post_cell_check_count]):
						cell_sheet.write(post_cell_counter, 4, "V")
					post_cell_check_count += 1
					post_cell_counter += 1

		# check postcheck RRU status	
		elif re.search("AuxPlugInUnit", line):
			blocks = line.split()
			if (len(blocks) == 6):
				if 'AuxPlugInUnit' in blocks[5]:
					rru_term = blocks[5].split("=")
					#print(rru_term[len(rru_term) - 1], blocks[2][1:-1], blocks[4][1:-1])
					ru_sheet.write(post_ru_counter, 3, blocks[2][1:-1] + "_" + blocks[4][1:-1], arial)
					if (blocks[2][1:-1] + "_" + blocks[4][1:-1] != pre_ru_st[post_ru_check_count]):
						ru_sheet.write(pre_cell_couter, 4, "V")
					post_ru_check_count += 1
					post_ru_counter += 1

		# check postcheck alarm:
		elif re.search('Nr of active alarms', line):
			blocks = line.split()
			alarms_num = int(blocks[len(blocks) - 1])
			if (alarms_num != 0):
				for count in range(alarms_num):
					post_alarm_lines.append(i+count+4)

		if i in post_alarm_lines:
			#print(line)
			post_alarm_count += 1
			post_alarm_datas.append(line)

		# List desire checking MOs and attributes:
		if re.search('get', line):
			blocks = line.split()
			#print(blocks)
			if (enb_name in blocks[0]):
				# if len == 3: enb_name> get MO
				if (len(blocks) == 3):
					post_check_mo.append(blocks[len(blocks) - 1])

				# if len == 4: enb_name> get MO attribute
				elif (len(blocks) >= 4):
					post_check_attr.append(blocks[len(blocks) - 1])
					post_check_attr_line.append(i + 6)

		if re.search('pst', line):
			blocks = line.split()
			if (enb_name in blocks[0]):
				pst_lines = i + 13


	#===============================================================#
	#			   pre-check post-check alarm compare				#
	#===============================================================#
	# [0]:type, [1]:mo, [2]:reason
	pre_alarm_check = [[], [], []]
	
	if len(post_alarm_datas) != 0:
		fit_line = []
		for post in range(len(post_alarm_datas)):
			post_alarm_check = []
			post_term = post_alarm_datas[post].split('   ')
			post_alarm_info = post_term[0].split()
			post_alarm_type = post_alarm_info[3]
			if (len(post_alarm_info) > 4):
				for rest in range(4, len(post_alarm_info)):
					post_alarm_type += ' '
					post_alarm_type += post_alarm_info[rest]
			post_alarm_exp = post_term[len(post_term) - 1].split('(')
			post_alarm_mo = post_alarm_exp[0]
			post_alarm_reason = '(' + post_alarm_exp[1][:-1]

			post_alarm_check.append(post_alarm_type)
			post_alarm_check.append(post_alarm_mo)
			post_alarm_check.append(post_alarm_reason)


			if (len(pre_alarm_datas) != 0):
				fit_line = list(range(len(pre_alarm_datas)))

				# Build pre-alarm check list only in first time
				if (post == 0):
					for pre in range(len(pre_alarm_datas)):
						pre_term = pre_alarm_datas[pre].split('   ')
						pre_alarm_info = pre_term[0].split()
						pre_alarm_type = pre_alarm_info[3]
						if (len(pre_alarm_info) > 4):
							for rest in range(4, len(pre_alarm_info)):
								pre_alarm_type += ' '
								pre_alarm_type += pre_alarm_info[rest]
						pre_alarm_exp = pre_term[len(pre_term) - 1].split('(')
						pre_alarm_mo = pre_alarm_exp[0]
						pre_alarm_reason = '(' + pre_alarm_exp[1][:-1]

						pre_alarm_check[0].append(pre_alarm_type)
						pre_alarm_check[1].append(pre_alarm_mo)
						pre_alarm_check[2].append(pre_alarm_reason)

				# check term: [0] = type, [1] = MO, [2] = reason
				for check_term in range(3):
					if fit_line != None:
						for alarm_num in fit_line:
							remove = []
							# check type and MO
							if (check_term != 2):
								#print("pre = ", post_alarm_check[check_term], "post = ", pre_alarm_check[check_term][alarm_num])
								if (post_alarm_check[check_term] != pre_alarm_check[check_term][alarm_num]):
									remove.append(alarm_num)

						# check reason
							elif (check_term == 2):
								if (len(post_alarm_check[check_term]) > len(pre_alarm_check[check_term][alarm_num])):
									remove.append(alarm_num)

						# remove unfit alarms
							if remove != []:
								for i in range(len(remove)):
									fit_line.remove(remove[i])

				# This alarm has a fit alarm in pre-check, the alarm should be record
				if (fit_line != []):
					#print(post_alarm_check)
					alarm_sheet.write(alarm_line_count, 0, enb_name, arial)
					alarm_sheet.write(alarm_line_count, 1, post_alarm_type, arial)
					alarm_sheet.write(alarm_line_count, 2, post_alarm_mo, arial)
					alarm_sheet.write(alarm_line_count, 3, post_alarm_reason, arial)
					alarm_line_count += 1
					if (len(post_alarm_type) > l_al_type) and len(post_alarm_type) <= 36:
						l_al_type = len(post_alarm_type)
					if (len(post_alarm_mo) > l_al_mo) and len(post_alarm_mo) <= 36:
						l_al_mo = len(post_alarm_mo)
					if (len(post_alarm_reason) > l_al_re) and len(post_alarm_reason) <= 36:
						l_al_re = len(post_alarm_reason)
				#print(post_alarm_type, post_alarm_mo, post_alarm_reason) 
					
			# There is no problem in pretcheck, so ervry alarm should be record
			else:
				alarm_sheet.write(alarm_line_count, 0, enb_name, arial)
				alarm_sheet.write(alarm_line_count, 1, post_alarm_type, arial)
				alarm_sheet.write(alarm_line_count, 2, post_alarm_mo, arial)
				alarm_sheet.write(alarm_line_count, 3, post_alarm_reason, arial)
				alarm_sheet.write(alarm_line_count, 4, "V")
				alarm_line_count += 1
				if (len(post_alarm_type) > l_al_type):
					l_al_type = len(post_alarm_type)
				if (len(post_alarm_mo) > l_al_mo):
					l_al_mo = len(post_alarm_mo)
				if (len(post_alarm_reason) > l_al_re):
					l_al_re = len(post_alarm_reason)

	# Find the MO's searching targets 
	if (site_num == 0):
		# Set searching target
		for i in range(len(post_check_mo)):
			blocks = post_check_mo[i].split(",")
			post_check_mo_find.append(blocks[len(blocks) - 1])

		# Set sheet naming rule
		for i in range(len(post_check_mo_find)):
			blocks = post_check_mo_find[i].split("=")
			mo_sheet_name.append(blocks[0])

		# Create MOs' worksheet
		for mo in range(len(mo_sheet_name)):
			mo_sheet_ls.append(workbook.add_worksheet(mo_sheet_name[mo]))

		# Set MO worksheet basic attribute
		for i in range(len(mo_sheet_name)):
			mo_sheet_ls[i].write(0, 0, "Site name", arial)
			mo_sheet_ls[i].write(0, 1, "parent", arial)
			mo_sheet_ls[i].write(0, 2, "MO name", arial)
			# Reside attributes start from (0, 3)

		# Create MO numbers lists to save mo's name
		for mo in range(len(mo_sheet_name)):
			mo_attr_name.append([])
			mo_line_count.append(1)

	# Create pst sheet
	if pst_lines != None:
		pst_sheet = workbook.add_worksheet('Pst')
		pst_sheet.write(0, 0, 'Site name', arial)
		pst_sheet.write(0, 1, 'Proxy', arial)
		pst_sheet.write(0, 2, 'Scanner name', arial)
		pst_sheet.write(0, 3, 'State', arial)

	# Reset the file reader pointer
	post_file.seek(0)

	# Indicate which MOs and attribute is been searched
	attr = 0
	mo = 0

	# Searching flags
	attr_detect = bool(0)
	pst_detect = bool(0)
	mo_detect = bool(0)
	mo_record = bool(0)
	mo_struct_detect = bool(0)
	mo_element_detect = bool(0)

	# Set an empty string for saving attribute name
	mo_name = None
	attr_name = None
	attr_value = None
	struct_id = None
	struct_name = None
	target_mo_name = None

	for i, line in enumerate(post_file, 1):
		#===============================================================================#
		# 					Indicate how to find desire attributes						#
		#===============================================================================#
		# Find first attribute, which is in get command line
		if (len(post_check_attr) != 0):
			if i == post_check_attr_line[attr]:
				if re.search('=====', line) and attr_detect == 0:
					if (attr != len(post_check_attr) - 1):
						attr += 1
				else:
					attr_detect = 1

			if attr_detect == 1 and re.search('=====', line):
				attr_detect = 0
				if (attr != len(post_check_attr) - 1):
					attr += 1
			if attr_detect == 1:
				blocks = line.split()
				attribute_value = blocks[2]
				if (len(blocks) > 3):
					for rest in range(3, len(blocks)):
						attribute_value += " "
						attribute_value += blocks[rest]
				attr_sheet.write(attr_counter, 0, enb_name, arial)
				attr_sheet.write(attr_counter, 1, blocks[0], arial)
				attr_sheet.write(attr_counter, 2, blocks[1], arial)
				attr_sheet.write(attr_counter, 3, attribute_value, arial)
				attr_counter += 1
				if (site_num == 0):
					if (len(blocks[0]) > l_mo_name):
						l_mo_name = len(blocks[0])
					if (len(blocks[1]) > l_attr_name):
						l_attr_name = len(blocks[1])
					if (len(blocks[2]) > l_value):
						l_value = len(blocks[2])

		#===============================================================================#
		#						Indicate how to find pst 								#
		#===============================================================================#
		if pst_lines != None:
			if i == pst_lines:
				if re.search('=====', line) and attr_detect == 0:
					pass
				else:
					pst_detect = 1

			if pst_detect == 1 and re.search('=====', line):
				pst_detect = 0

			if pst_detect == 1:
				blocks = line.split()
				pst_sheet.write(pst_line_count, 0, enb_name, arial)
				pst_sheet.write(pst_line_count, 1, blocks[0], arial)
				pst_sheet.write(pst_line_count, 2, blocks[1], arial)
				pst_sheet.write(pst_line_count, 3, blocks[2], arial)
				pst_line_count += 1
				if (site_num == 0):
					if (len(blocks[1]) > l_scanner_name):
						l_scanner_name = len(blocks[1])

		#===============================================================================#
		# 						Indicate how to find desire MOs							#
		#===============================================================================#
		
		# Find first MO, which is in get command line
		if (len(post_check_mo_find) != 0):
			if re.search(post_check_mo_find[mo], line) and mo_detect == 0:
				mo_term = line.split()
				if (len(mo_term) == 2):
					mo_tree_term = mo_term[1].split(',')
					target_mo_term = mo_tree_term[len(mo_tree_term) - 1].split('=')
					target_mo_parent = mo_tree_term[0]
					if (len(mo_tree_term) - 1 > 1):
						for parent in range(1, len(mo_tree_term) - 1):
							target_mo_parent += ','
							target_mo_parent += mo_tree_term[parent]

					target_mo_name = target_mo_term[0]
					#print(target_mo_parent, target_mo_name, target_mo_value)
					mo_detect = 1

			# If already detect MO, record it from '=' until find another '='
			if re.search('=====', line) and mo_detect == 1 and mo_record == 0:
				mo_record = 1
				# Record necessary component in every MO
				mo_sheet_ls[mo].write(mo_line_count[mo], 0, enb_name, arial)
				mo_sheet_ls[mo].write(mo_line_count[mo], 1, target_mo_parent, arial)
				mo_sheet_ls[mo].write(mo_line_count[mo], 2, target_mo_name,arial)

			elif re.search('=====', line) and mo_detect == 1 and mo_record == 1:
				mo_record = 0
				mo_line_count[mo] += 1

			# Record attriutes data in MOs
			elif mo_record == 1:
				blocks = line.split()
				# Struct detected by keyword "t[num] ="
				if (blocks[len(blocks) - 1] == '='):
					struct_num = re.search(r'\d+', blocks[1])
					struct_name = blocks[0]
					attr_name = blocks[0]
					attr_value = struct_num[0] + " struct"
					#print(target_mo_name, " ", attr_name, " ", attr_value)

				# Struct detected by keyword "Struct{num}"
				elif re.search('Struct', blocks[len(blocks) - 1]):
					struct_num = re.search(r'\d+', blocks[1])
					struct_name = blocks[0]
					attr_name = blocks[0]
					struct_id = blocks[0]
					attr_value = struct_num[0] + " struct"
					#print(target_mo_name, " ", attr_name, " ", attr_value)

				# Struct element statement, by keyword ">>>" 
				elif blocks[0] == '>>>':
					# This line indicate struct information
					if re.search("Struct", line) and len(blocks) > 2:
						struct_id = blocks[1]
						ele_num = blocks[3]
						attr_name = struct_name + '.' + struct_id
						attr_value = ele_num + ' members'
						#print(target_mo_name, ' ', attr_name, ' ', attr_value)
					else:
						attr_name = target_mo_name + '.' + struct_id + '.' + blocks[1]
						attr_value = blocks[len(blocks) - 1]
						#print(target_mo_name, " ", attr_name, " ", attr_value)

				# Normal attribute and values
				else:
					# There is no value in this attribute
					if (len(blocks) == 1):
						attr_name = blocks[0]
						attr_value = None
						#print(target_mo_name, " ", attr_name, " ", attr_value)
					else:
						attr_name = blocks[0]
						attr_value = blocks[1]
						if (len(blocks) > 2):
							for rest in range(2, len(blocks)):
								attr_value += " "
								attr_value += blocks[rest]
						#print(target_mo_name, " ", attr_name, " ", attr_value)

				if target_mo_name == mo_sheet_name[mo]:
					if attr_name not in mo_attr_name[mo]:
						mo_attr_name[mo].append(attr_name)
						x = len(mo_attr_name[mo]) + 2
						#y = mo_line_count[mo]
						mo_sheet_ls[mo].write(0, x , attr_name, arial)
						mo_sheet_ls[mo].write(mo_line_count[mo], x, attr_value, arial)
						#print(attr_name, attr_value)
					else:
						x = mo_attr_name[mo].index(attr_name) + 3
						mo_sheet_ls[mo].write(mo_line_count[mo], x, attr_value, arial)
						#print(attr_name, attr_value)


		# Already find all MOs, reset detect flags
			if re.search('Total:', line) and mo_detect == 1:
				mo_detect = 0
				if (mo != len(post_check_mo_find) - 1):
					mo += 1

	# Close file
	post_file.close()

# Set excel file cell width
cell_sheet.set_column(0, 0, l_enb_name + 3)
cell_sheet.set_column(1, 1, l_cell_name + 3)
cell_sheet.set_column(2, 2, l_cell_st + 10)
cell_sheet.set_column(3, 3, l_cell_st + 10)
cell_sheet.set_column(4, 4, len('truoble shoot'))

ru_sheet.set_column(0, 0, l_enb_name + 3)
ru_sheet.set_column(1, 1, l_ru_name + 3)
ru_sheet.set_column(2, 2, l_ru_st + 10)
ru_sheet.set_column(3, 3, l_ru_st + 10)
ru_sheet.set_column(4, 4, len('trouble shoot'))

alarm_sheet.set_column(0, 0, l_enb_name + 3)
alarm_sheet.set_column(1, 1, l_al_type + 3)
alarm_sheet.set_column(2, 2, l_al_mo + 10)
alarm_sheet.set_column(3, 3, l_al_re + 3)
alarm_sheet.set_column(4, 4, len('trouble shoot'))

attr_sheet.set_column(0, 0, l_enb_name + 3)
attr_sheet.set_column(1, 1, l_attr_name + 3)
attr_sheet.set_column(2, 2, l_attr_name + 5)
attr_sheet.set_column(3, 3, l_value + 3)

# Set pst sheet column width
if pst_lines != None:
	pst_sheet.set_column(0, 0, l_enb_name + 3)
	pst_sheet.set_column(1, 1, 5)
	pst_sheet.set_column(2, 2, l_scanner_name + 3)
	pst_sheet.set_column(3, 3, len('SUSPENDED') + 5)

# Set MO sheet column width
if (mo_sheet_ls != []):
	for i in range(len(mo_sheet_ls)):
		mo_sheet_ls[i].set_column(0, 0, l_enb_name + 3)
		mo_sheet_ls[i].set_column(1, len(mo_attr_name[i]), 20)

# Close the xlsx file
workbook.close()

# Calculate program runtime
stop_t = t.default_timer()
runtime = stop_t - start_t
print('Total runtime: ', runtime)

