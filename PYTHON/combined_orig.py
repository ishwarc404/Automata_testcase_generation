
import sys
import nltk
from nltk.tokenize import word_tokenize #to tokenize
from nltk.corpus import stopwords #to remove the stop words
from stemming.porter2 import stem #for stemming
import string #for a list of all the alphabets
import random
import string
import numpy as np

import re
from collections import Counter


#PRE-INITIAL STAGE
#SPELL CHECK CODE
#VERY IMPORTANT
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))




#INITAL STAGE

#CHECKING OF THE CORRECTNESS OF THE INPUT
print(nltk.tag.pos_tag(['bb']))
error_code = 0  
error_log = [] #his variable will be sotring all the errors that the program throws at us.
entered_string = "Generate strings having length 6 with a followed by baab "
tup = ('aa','ab','bb','ba')
new_string = []
#lets make a copy of entered_striing
copy_entered_string  =  entered_string[:]
for i in copy_entered_string.split():
	if( ("'s" not in i) and ( nltk.tag.pos_tag([i])[0][1] != 'DT') and len([x for x in tup if x not in i])==0):
		new_i = correction(i)
		new_string.append(new_i)
	else:
		new_string.append(i)


new_string  = ' '.join(new_string)
print(new_string)
######## PREPROCESSING ! #####################

#step 1: tokenize the string
tokenized_words = (word_tokenize(new_string))

#step2 : tagging # this tells which category of speech do each of those words belong to
tagged_words = nltk.pos_tag(tokenized_words)
print(tagged_words)


#step 3 : chunking. basically grouping together the tokenized words to form bigger chunks
chunkGram = r"""Chunk: {<VBG><IN><CD>}  #EACH OF THESE CHUNKERS WERE DECIDED BY TRIAL AND ERROR METHOD
				Chunk: {<VBG><IN><NN>}
				Chunk: {<VBG><IN><NNP>}
				Chunk: {<VBG><IN><JJ>} #ending with ab
				Chunk: {<VBG><IN><DT>}
				Chunk: {<VBG><DT><NN>*}
				Chunk: {<NN><IN><CD>*}
				Chunk: {<VBN><JJ><CD>}
				Chunk: {<NN><IN><DT>}
				Chunk: {<NN><CD>}  #length 5
				Chunk: {<JJ><CD>}  #length 5
				Chunk: {<NN><VBD><CD>}  #length 5
				Chunk: {<RB><DT><POS>} 
				Chunk: {<JJ><NNP><POS>}
				Chunk: {<VBZ><DT><POS>}
				Chunk: {<PDT><DT><POS>}
				Chunk: {<RB><NN><POS>}
				Chunk: {<RB><VBP><POS>}
				Chunk: {<JJ><NN><POS>} 
				hunk: {<JJ><NN>} 
				Chunk: {<RB><DT>}"""   ##this will select "starting with 1 (verb/preposition/cardinal number"
chunkParser  = nltk.RegexpParser(chunkGram)
result = chunkParser.parse(tagged_words) 



##THE FOLLOWING CODE RETRIEVES THE CHUNKED DATA WITHOUT THE POS TAGS
chunked_terms = []
for e in result.subtrees(filter=lambda t: t.label() == 'Chunk'):
	if isinstance(e, tuple):
		chunked_terms.append([ e[0] ])
	else:
		chunked_terms.append([w for w, t in e])


#Step 4: STEMMING 
#pip install stemming==1.0 <-- used this stemmer
for i in chunked_terms:
	k = 0
	i[k] = (stem(i[k]))


#Step5: Removal of Stop Words and Metacharacters 
stop_words = set(stopwords.words("english"))
filtered_sentence = []

##ALL THE FOLLOWING DRAMA IS EXCEPTION AND ERROR HANDLING
alphabets = "abcdefghijklmnopqrstuvwxyz" 
alphabets = list(alphabets)
filter_list = list(set(stop_words) - set(alphabets))

for i in chunked_terms:
	for j in i:
		if (j not in filter_list) :
			filtered_sentence.append(j)


#REMOVING THE 's and the metacharacters
for i in filtered_sentence:    
	if i == "'s":
		filtered_sentence.remove("'s")

#Removing the keyword string
if "string" in filtered_sentence:
	filtered_sentence.remove("string")


#NEED TO HANDLE "ATLEAST" and "ATMOST" KEYWORD HERE ITSELF OR ELSE THE NEXT LOOP WILL GIVE ERROR
atleastlength_flag = 0
if "atleast" in filtered_sentence:
	filtered_sentence.remove("atleast")
	atleastlength_flag = 1

atmostlength_flag = 0
if "atmost" in filtered_sentence:
	filtered_sentence.remove("atmost")
	atmostlength_flag = 1


print(len(filtered_sentence))
#INITAL EXCEPTION HANDLING
#WHAT HAPPENS IF THE INTIAL LENGTH IS 0 OF THE STRING or if there is nothing to chunk in the inputted string
if(len(filtered_sentence) == 0) : #means if it is 0
	error_code = 0
	error_log.append(error_code)




#NOW WE NEED TO DO SOME MORE ERROR HANDLING
#EXAMPLE THE NUMBER OF a's cannot be odd and even at the same time
#so basically put a simple check as follows
exceptionfunclist = ['start','end','length']
for i in range(0,len(filtered_sentence)-2,2):
	if(filtered_sentence[i]!=filtered_sentence[i+2] and (filtered_sentence[i] not in exceptionfunclist)): #means if the two functions are the different (example odd and even)
		#check if the parameters are the same too
		if(filtered_sentence[i+1]==filtered_sentence[i+2+1]) :
			print("ERR0R: The same character cannot have both even and odd numbered occurances")
			exit()
			error_log.append(())

	elif(filtered_sentence[i]==filtered_sentence[i+2]): #removing multiple occurances of the same function
		if(filtered_sentence[i+1]==filtered_sentence[i+2+1]):
			print(filtered_sentence)
			filtered_sentence.pop(i+2)
			filtered_sentence.pop(i+2)


#THIS PART OF THE CODE PREPARES THE FILTERED_SENTENCE FOR THE STAGE 2 INITIAL ERROR HANDLING PART
#WE REPLACE EVEN WITH EVEN1,EVEN2 AND SO ON and similarly FOR ODD as there is only a single even or
#odd function definition in stage2 
even_indices = [i for i, x in enumerate(filtered_sentence) if x == "even"]
odd_indices = [i for i, x in enumerate(filtered_sentence) if x == "odd"]

for i in range(0,len(even_indices)):
	filtered_sentence[even_indices[i]] = 'even'+str(i+1) #coz i starts with 1

for i in range(0,len(odd_indices)):
	filtered_sentence[odd_indices[i]] = 'odd'+str(i+1) #coz i starts with 1

print(filtered_sentence)


################################################################################################################################################
################################################################################################################################################
################################################################ STAGE 2 #########################################################################
################################################################################################################################################
################################################################################################################################################



#VARIABLE DECLARATIONS
string_nonfinal = []  #Main DS where everything will be stored


#FUNCTION LIST FUNCTION DEFINITIONS
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






func_list  = [[0,start,""],[0,length,0],[0,end,"",],[0,even1,"",],[0,even2,"",],[0,odd1,""],[0,odd2,""]]
 #initial func_list definition #start and end are variable length, coz might include last parameter as length
filtered_sentence_length_copy = filtered_sentence[:] #this is used as coz we call the initialise functions multiple times with multiple lengths
even_odd_count = 0 #tells how many times the func was executed
even_odd_flag = [] #these flags will tell us what functions were actually executed

###NEED TO WORK ON THIS SYMBOLS AS WE HAVE HARDCODED IT HERE
symbols =["a","b"] #need to pass this as an argument for length function 
start_length = 0
end_length = 0 




#FUNCTION 1
def initialize(length):
	for i in range(len(filtered_sentence_length_copy)):
		if(filtered_sentence_length_copy[i]=="length"):
			filtered_sentence_length_copy[i+1] = length



	#activating the func_list
	for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
		for j in func_list :	
				   #will not work as we cant compare "start" to function start
			
			if filtered_sentence_length_copy[i] == j[1].__name__:
				j[0] = 1
				j[2] = filtered_sentence_length_copy[i+1]


			
	start_end_length_func()



#FUNCTION 2
def start_end_length_func():
	#LETS CALCULATE THE START LENGTH AND END LENGTH
	global start_length
	global end_length


	for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
		if filtered_sentence_length_copy[i]=="start":
			start_length = len(filtered_sentence_length_copy[i+1])
		if filtered_sentence_length_copy[i]=="end":
			end_length = len(filtered_sentence_length_copy[i+1])

	

#FUNCTION 3 #MOST IMPORTANT FUNCTION
def activated_function_calls():
	#outer order of start,end,length
	#inner order of state,function_name,parameter
	#CALLING THE FUNCTIONS USING EVAL
	#FUNCTION GETS CALLED ONLY IF STATE IS 1	
	# print(func_list)
	for i in func_list:   #checking if the function state is 1 and calling
		if i[0]==1:
			third_para = str(i[2])
			i[1](third_para)



 

def even(character):

	global even_odd_count
	even_odd_count = even_odd_count + 1

	countfinal  = 0
	start_end_length_func()
	#lets define some flags
	start_full = 0
	end_full = 0

	if(start_length == 0 and end_length == 0):
		countfinal = 0
		count2 = string_nonfinal[0].count(character) 

	elif(start_length != 0 and end_length == 0):
		countfinal = string_nonfinal[0].count(character)
		count2 = string_nonfinal[1].count(character) 
		start_full = 1 #means  start contains something

	elif(start_length == 0 and end_length != 0):
		countfinal = string_nonfinal[1].count(character)
		count2 = string_nonfinal[0].count(character) 
		end_full = 1 #means  end contains something
	elif(start_length != 0 and end_length != 0):
		countfinal = string_nonfinal[0].count(character) + string_nonfinal[2].count(character)

		count2 = string_nonfinal[1].count(character) 
		start_full = 1
		end_full = 1 #means  end contains something

	symbols_copy = symbols[:]
	symbols_copy.remove(character)
	replacement_character = random.choice(symbols_copy)
	#replacement_character = "b"
	if((countfinal%2==0 and count2%2==0) or (countfinal%2!=0 and count2%2!=0)): 
		#means if the total number of characters is even/odd in both places, the entire thing will have a total even occurances
		return
	else:
		#error
		#error is in replace function #SUPER IMPORTANT 
		if(start_full == 1 and end_full == 1):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[1]):
				string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
				
				return string_nonfinal
			else:
				string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
				
				return string_nonfinal

		elif(start_full == 1 and end_full ==0):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[1]):
				string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal

		elif(start_full == 0 and end_full ==1):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[1]):
				string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal

		elif(start_full == 0 and end_full ==0):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[0]):
				string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal



def odd(character):

	global even_odd_count
	even_odd_count = even_odd_count + 1

	countfinal  = 0

	start_end_length_func()
	#lets define some flags
	start_full = 0
	end_full = 0

	if(start_length == 0 and end_length == 0):
		countfinal = 0
		count2 = string_nonfinal[0].count(character) 

	elif(start_length != 0 and end_length == 0):
		countfinal = string_nonfinal[0].count(character)
		count2 = string_nonfinal[1].count(character) 
		start_full = 1 #means  start contains something

	elif(start_length == 0 and end_length != 0):
		countfinal = string_nonfinal[1].count(character)
		count2 = string_nonfinal[0].count(character) 
		end_full = 1 #means  end contains something
	elif(start_length != 0 and end_length != 0):
		countfinal = string_nonfinal[0].count(character) + string_nonfinal[2].count(character)

		count2 = string_nonfinal[1].count(character) 
		start_full = 1
		end_full = 1 #means  end contains something



	symbols_copy = symbols[:]
	symbols_copy.remove(character)
	replacement_character = random.choice(symbols_copy)
	#replacement_character = "b"
	if((countfinal%2!=0 and count2%2==0) or (countfinal%2==0 and count2%2!=0)): 
		#means if the total number of characters is even/odd in both places, the entire thing will have a total even occurances
		return
	else:
		#error
		#error is in replace function
		if(start_full == 1 and end_full == 1):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[1]):
				string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal

		elif(start_full == 1 and end_full ==0):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[1]):
				string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal

		elif(start_full == 0 and end_full ==1):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[1]):
				string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal

		elif(start_full == 0 and end_full ==0):
			#means both start and end exist and still the number of that character is not even
			if(character in string_nonfinal[0]):
				string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
				# print("here")
				return string_nonfinal
			else:
				string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
				# print("here")
				return string_nonfinal








#VALIDATION OF THE STRINGS GENERATED AFTER GOING THROUGH ODD AND EVEN FUNCTIONS
def even_odd_valid():
	 
	 if(start_length == 0 and end_length ==0) :
	 	start_full = 0
	 	end_full = 0
	 elif(start_length != 0 and end_length ==0) :
	 	start_full = 1
	 	end_full = 0
	 elif(start_length == 0 and end_length !=0) :
	 	start_full = 0
	 	end_full = 1
	 elif(start_length != 0 and end_length !=0) :
	 	start_full = 1
	 	end_full = 1


	 exit_flag = 0

	 #BASICALLY THIS FUNCTION WILL COUNT AND CHECK THE OCCURANCES OF THE PARTICULAR CHARACTER
	 for i in even_odd_flag:
	 	if i[0]=='even':
	 		if(start_full == 1 and end_full == 1):
		 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  + string_nonfinal[2].count(i[1])  
		 		if count%2 != 0: #means its not acutally even
		 			exit_flag = 1
		 	elif(start_full == 1 and end_full == 0): #means only start string exists
		 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  
		 		if count%2 != 0: #means its not acutally even
		 			exit_flag = 1
		 	elif(start_full == 0 and end_full == 1): #means only end string exists
		 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  
		 		if count%2 != 0: #means its not acutally even
		 			exit_flag = 1

 		elif i[0]=='odd':
	 		if(start_full == 1 and end_full == 1):
		 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  + string_nonfinal[2].count(i[1])  
		 		if count%2 == 0: #means its not acutally odd
		 			exit_flag = 1
		 	elif(start_full == 1 and end_full == 0): #means only start string exists
		 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  
		 		if count%2 == 0: #means its not acutally odd
		 			exit_flag = 1
		 	elif(start_full == 0 and end_full == 1): #means only end string exists
		 		count = string_nonfinal[0].count(i[1])  + string_nonfinal[1].count(i[1])  
		 		if count%2 == 0: #means its not acutally odd
		 			exit_flag = 1

	 	if(exit_flag == 1):
	 		print("ERROR ------ String cannot be generated with the following combination") 
	 		exit()


########################################################################################################################
########################################################################################################################
########################################################################################################################
################################################# MAIN #################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################



#LETS GET THE LENGTH OF THE STRING THAT NEEDS TO BE GENERATED
initiallength =  0
for i in range(len(filtered_sentence)):
	if(filtered_sentence[i]=="length"):
		initiallength = int(filtered_sentence[i+1])


start_end_length_func() #getting the total length of the start and end characters
total_beginlength = start_length+end_length



##################### FINAL PRINTINTG CASE 1


setofstrings = [] 

if(atmostlength_flag == 1):
	for i in range(200):
		for i in range(total_beginlength,initiallength+1):
			string_nonfinal = []

			initialize(i) #pass the number of characters you want to generate here

			activated_function_calls()

			if(even_odd_count ==2):   #means only if the function was executed twice the strings need to go through a validity check
				even_odd_valid()

			final_string = "".join(string_nonfinal) #joins all the strings present in the list

			setofstrings.append(final_string)

	
	setofstrings = set(setofstrings)
	setofstrings = sorted(setofstrings, key=len)
	print(setofstrings)


##################### FINAL PRINTING CASE 2


setofstrings = [] 
if(atleastlength_flag == 1):
	for i in range(200):
		for i in range(initiallength,initiallength + 10): #10 is a random number
			string_nonfinal = []
			initialize(i) #pass the number of characters you want to generate here
			activated_function_calls()

			if(even_odd_count ==2):
				even_odd_valid()

			
			final_string = "".join(string_nonfinal) #joins all the strings present in the list
			
			setofstrings.append(final_string)

	setofstrings = set(setofstrings)
	setofstrings = sorted(setofstrings, key=len)
	print(setofstrings)


#means if those particular set of codes were executed, don't execute the others
if(atmostlength_flag == 1 or atleastlength_flag == 1):
	exit()


##################### FINAL PRINTINTG CASE 3

setofstrings = [] 
for i in range(200):
	string_nonfinal = []
	initialize(initiallength) #pass the number of characters you want to generate here
	activated_function_calls()

	if(even_odd_count ==2):
		even_odd_valid()

	#print(string_nonfinal)
	final_string = "".join(string_nonfinal) #joins all the strings present in the list
	setofstrings.append(final_string)  #prints out the final string

 
setofstrings = set(setofstrings)
setofstrings = sorted(setofstrings, key=len)
print(setofstrings)





