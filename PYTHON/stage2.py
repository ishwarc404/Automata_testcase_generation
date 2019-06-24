
 ##TO DO:
'''
1. TALK TO PREET MA'AM ABOUT THE SUBSTRING PART
2. DEFINE THE ODD FUNCTION SUPER IMPORTANT --- DONE DONE DONE DONE --- just one line differnece
3. ACTIVATING FUNCTION LIST needs exception handling as the filtered sentence might not be in the same order
4. FUNCTION LIST WONT BE ACTIVIATED IF even a and even b is there. coz the function will be called only once. so in stage 1, that stuff neeeds to be taken care of
'''
import random
import string
import numpy as np


string_nonfinal = []
filtered_sentence = ['start','a','length','10','end','b']   ###NEED TO WORK ON EVEN PART AS IT TAKES ONLY ONE CHARACTER
func_list  = [[0,"start","",],[0,"length",0],[0,"end","",],[0,"even1","",],[0,"even2","",],[0,"odd1",""],[0,"odd2",""]] #initial func_list definition #start and end are variable length, coz might include last parameter as length
filtered_sentence_length_copy = filtered_sentence[:]

even_odd_count = 0 
even_odd_flag = [] #these flags will tell us what functions were actually executed
###NEED TO WORK ON THIS SYMBOLS AS WE HAVE HARDCODED IT HERE
symbols =["a","b"] #need to pass this as an argument for length function 
start_length = 0
end_length = 0 

def initialize(length):
	for i in range(len(filtered_sentence_length_copy)):
		if(filtered_sentence_length_copy[i]=="length"):
			filtered_sentence_length_copy[i+1] = length

	
	#activating the func_list
	for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
		#print("in loop")
		for j in func_list :				   #will not work as we cant compare "start" to function start
			if filtered_sentence_length_copy[i]==j[1]:
				j[0] = 1
				j[2] = filtered_sentence_length_copy[i+1]


	start_end_length_func()

def start_end_length_func():
	#LETS CALCULATE THE START LENGTH AND END LENGTH
	global start_length
	global end_length


	for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
		if filtered_sentence_length_copy[i]=="start":
			start_length = len(filtered_sentence_length_copy[i+1])
		if filtered_sentence_length_copy[i]=="end":
			end_length = len(filtered_sentence_length_copy[i+1])

	# print(filtered_sentence_length_copy)


def activated_function_calls():
	#outer order of start,end,length
	#inner order of state,function_name,parameter
	#CALLING THE FUNCTIONS USING EVAL
	#FUNCTION GETS CALLED ONLY IF STATE IS 1	
	# print(func_list)
	for i in func_list:   #checking if the function state is 1 and calling
		if i[0]==1:
			third_para = str(i[2])
			code = i[1]+"("+"'"+third_para+"'"+")"
			#print(code)
			eval(code)


def start(x):
	string_nonfinal.append(x)
	return


def length(y):
	y = int(y)
	y  = y - int(start_length) - int(end_length) #obviously
	if(y<0):
		print("ERROR --------length specified is too short")
		exit()
	randomstr = ''.join([np.random.choice(symbols) for n in range(y)]) 
	string_nonfinal.append(randomstr)
	return	

def end(z):
	string_nonfinal.append(z)
	return
 

def even(character):

	global even_odd_count
	even_odd_count = even_odd_count + 1


	#count1 = string_nonfinal[0].count(character) #WILL NOT WORK AS COUNT1 IS HARDCODED TO THE START STRING
	#HENCE WE NEED TO USE A IF CLAUSE
	##WHAT IF BOTH START AND END IS THE SAME CHARACTER
	countfinal = string_nonfinal[0].count(character) + string_nonfinal[2].count(character)
	#print(countfinal)
	count2 = string_nonfinal[1].count(character)

	#finding the replacement character
	symbols_copy = symbols[:]
	symbols_copy.remove(character)
	replacement_character = random.choice(symbols_copy)
	#replacement_character = "b"
	if((countfinal%2==0 and count2%2==0) or (countfinal%2!=0 and count2%2!=0)):
		#print("here")
		return
	else:
		if (countfinal + count2 == 1):
			#print("there1")
			string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
			return string_nonfinal
		else:
			#this wont work if count1 is 1 and count2 is 0
			#print("there2")
			string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
			return string_nonfinal




def odd(character):

	global even_odd_count
	even_odd_count = even_odd_count + 1



	#count1 = string_nonfinal[0].count(character) #WILL NOT WORK AS COUNT1 IS HARDCODED TO THE START STRING
	#HENCE WE NEED TO USE A IF CLAUSE
	##WHAT IF BOTH START AND END IS THE SAME CHARACTER
	countfinal = string_nonfinal[0].count(character) + string_nonfinal[2].count(character)
	count2 = string_nonfinal[1].count(character)
	#. print(count2)
	#finding the replacement character
	symbols_copy = symbols[:]
	symbols_copy.remove(character)
	replacement_character = random.choice(symbols_copy)
	#replacement_character = "b"

	if((countfinal%2!=0 and count2%2==0) or (countfinal%2==0 and count2%2!=0)):  ##	this step is the only differnce between odd and even
		#print("here")
		return
	else:
		if (countfinal + count2 == 1):
			#print("there1")
			string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
			return string_nonfinal
		else:
			#this wont work if count1 is 1 and count2 is 0
			#print("there2")
			string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
			return string_nonfinal


def even1(character):
	even_odd_flag.append(['even',character])
	even(character)
	return

def even2(character):
	even_odd_flag.append(['even',character])
	even(character)
	return
def odd1(character):
	even_odd_flag.append(['odd',character])
	odd(character)
	return
def odd2(character):
	even_odd_flag.append(['odd',character])
	odd(character)
	return



def even_odd_valid():
	 #print("this function is running as the even or odd functions were called a total of 2 times \n which messes with the final result")
	 #print(even_odd_flag) 
	 exit_flag = 0
	 for i in even_odd_flag:
	 	if i[0]=='even':
	 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  + string_nonfinal[2].count(i[1])  
	 		if count%2 != 0: #means its not acutally even
	 			#print(count)
	 			exit_flag = 1
	 	elif i[0]=='odd':
	 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  + string_nonfinal[2].count(i[1])  
	 		if count%2 == 0: #means its not acutally even
	 			#print(count)
	 			exit_flag = 1
	 	if(exit_flag == 1):
	 		print("ERROR ------ String cannot be generated with the following combination") 
	 		exit()


########################################################################################################################
"""MAIN"""
initiallength =  0
for i in range(len(filtered_sentence)):
	if(filtered_sentence[i]=="length"):
		initiallength = int(filtered_sentence[i+1])

start_end_length_func() #getting the total length of the start and end characters
tot = start_length+end_length


##################### FINAL PRINTINTG CASE 1


setofstrings = [] ##so as to eliminated

# if(initiallength==0):
# 	print
# 	initiallength = 20 #some random number else it will be zero and wont work


if(atmostlength_flag == 1):
	for i in range(200):
		for i in range(tot,initiallength+1):
			string_nonfinal = []
			#print(i)
			initialize(i) #pass the number of characters you want to generate here
			activated_function_calls()

			if(even_odd_count ==2):
				even_odd_valid()

			#print(string_nonfinal)
			final_string = "".join(string_nonfinal) #joins all the strings present in the list
			# print(final_string)  #prints out the final string
			setofstrings.add(final_string)

	setofstrings = sorted(setofstrings, key=len)
	setofstrings = set(setofstrings)
	print(setofstrings)

##################### FINAL PRINTINTG CASE 2


setofstrings = [] ##so as to eliminated
if(atleastlength_flag == 1):
	for i in range(200):
		for i in range(initiallength,initiallength + 10): #10 is a random number
			string_nonfinal = []
			initialize(i) #pass the number of characters you want to generate here
			activated_function_calls()

			if(even_odd_count ==2):
				even_odd_valid()

			#print(string_nonfinal)
			final_string = "".join(string_nonfinal) #joins all the strings present in the list
			#print(final_string)  #prints out the final string
			setofstrings.append(final_string)

	setofstrings = set(setofstrings)
	setofstrings = sorted(setofstrings, key=len)
	print(setofstrings)



if(atmostlength_flag == 1 or atleastlength_flag == 1):
	exit()


##################### FINAL PRINTINTG CASE 3
setofstrings = [] ##so as to eliminated
for i in range(200):
	string_nonfinal = []
	initialize(initiallength) #pass the number of characters you want to generate here
	activated_function_calls()

	if(even_odd_count ==2):
		even_odd_valid()

	#print(string_nonfinal)
	final_string = "".join(string_nonfinal) #joins all the strings present in the list
	setofstrings.append(final_string)  #prints out the final string

print((set(setofstrings)))



