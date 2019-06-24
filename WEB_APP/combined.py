
import sys
import nltk
from nltk.tokenize import word_tokenize #to tokenize
from nltk.corpus import stopwords #to remove the stop words
from stemming.porter2 import stem #for stemming
import string #for a list of all the alphabets
import random
import string
import numpy as np
import ast
import re
from collections import Counter
import spell_check


#defining all the variables
start_length = 0
end_length = 0
even_odd_count = 0
initiallength =  0
atmostlength_flag = 0
atleastlength_flag = 0
setofstrings = set()

#VARIABLE DECLARATIONS
string_nonfinal = []  #Main DS where everything will be stored

#initial func_list definition #start and end are variable length, coz might include last parameter as length
filtered_sentence = []
filtered_sentence_length_copy = filtered_sentence[:] #this is used as coz we call the initialise functions multiple times with multiple lengths
even_odd_count = 0 #tells how many times the func was executed
even_odd_flag = [] #these flags will tell us what functions were actually executed

###NEED TO WORK ON THIS SYMBOLS AS WE HAVE HARDCODED IT HERE
symbols =["a","b"] #need to pass this as an argument for length function 
start_length = 0
end_length = 0 


#ERROR LOG ; LET'S STORE ALL THE ERROR'S THAT OCCUR AND MATCH WITH THE DICTIONARY
error_log  = {0:"NO ERROR" , 1:"ENTERED STRING IS EMPTY",2:"SAME CHARACTER CANNOT HAVE BOTH ODD AND EVEN OCCURANCES",3:"NO GENERATION FEATURES WERE INPUTTED",4:"NO STRINGS POSSIBLE WITH GIVEN ODD/EVEN COMBINATIONS"}
error_catch = []
error_update = 0
count_activated_func = 0


class test_class:

	def input(self,entered_string):  #AKA MAIN FUNCTION
		
		#FUNCTION 1
		#THIS IS THE FIRST FUNCTION THAT IS CALLED
		#THIS WILL ACT AS THE MAIN FUNCTION
		global error_catch
		global error_update
		global error_log
	
		#ERROR HANDLING
		if(len(entered_string)==0):
			error_catch.append([1,error_log[1]])  
			error_update = 1 #we update the length to keep track of its changes
			return(error_catch[-1])

		#LET US GET THE INPUT AND CALL THE SPELL CHECKER FUNCTION FIRST
		spell_checked_string = self.input_spellchecker(entered_string)
		
		#NOW THIS SPELL CHECKED STRING WILL GET PRE-PROCESSED AND WE WILL GET A FILTERED LIST AS RETURN, ATMOST AND ATLEAST FLAGS (GLOBAL) WILL ALSO BE SET
		#AKA STAGE1
		filtered_list = self.preprocessing(spell_checked_string)

		#LET'S SEE IF THE PREPROCESSING STAGE ENDED EARLIER AND GAVE US AN ERROR COZ OF THAT
		if(error_update == 1) : #means the error_catch variable was updated
			return(error_catch[-1])#then it returns to the gui the latest and freshest error


		#NOW THE FILTERED LIST WILL BE PASSED ONTO THE STAGE2 INITALIZATION CODE
		#THE INITIALIZATION CODE CALLS THE OTHER FUNCTIONS
		final_strings = self.stage2_initialize(filtered_list)

		#LET'S SEE IF THE INITIALIZATION STAGE ENDED EARLIER AND GAVE US AN ERROR COZ OF THAT
		if(error_update == 1) : #means the error_catch variable was updated
			return(error_catch[-1])#then it returns to the gui the latest and freshest error


		f = open("input.txt",'w')
		for i in final_strings:
			f.write(i+"\n")

		return("FINAL SET OF STRINGS GENERATED",final_strings)
	


	#ALL THESE FUNCTIONS NEED TO BE DEFINED HERE
	def start(self,x):
		global string_nonfinal
		string_nonfinal.append(x)
		return

	def length(self,y):
		global start_length
		global end_length
		global string_nonfinal
		y = int(y)
		self.start_end_length_func()
		y  = y - int(start_length) - int(end_length) #obviously
		if(y<0):
			print("ERROR --------length specified is too short")
			exit()
		
		randomstr = ''.join([np.random.choice(symbols) for n in range(y)]) 
		string_nonfinal.append(randomstr)
		return	

	def end(self,z):
		global string_nonfinal
		string_nonfinal.append(z)
		return


	def even1(self,character):
		even_odd_flag.append(['even',character])
		self.even(character)
		return

	def even2(self,character):
		even_odd_flag.append(['even',character])
		self.even(character)
		return
	def odd1(self,character):
		even_odd_flag.append(['odd',character])
		self.odd(character)
		return
	def odd2(self,character):
		even_odd_flag.append(['odd',character])
		self.odd(character)
		return

	def follow(self,str):
		global setofstrings
		start_follow = str[0:str.index("$")]
		end_follow = str[str.index("$")+1:]

		start_follow_length = len(start_follow)
		end_follow_length = len(end_follow)
		final_strings=[]

		def check(string):
			count_start_end = string.count(start_follow+end_follow)
			count_start = string.count(start_follow)
			if(count_start_end== count_start):
				final_strings.append(string)

		def double_check(string):
			i=0
			string_cpy = string[:]
			while(i<= len(string)):
				if(start_follow in string):
					i = string.index(start_follow)
					cut_str = string[(i+start_follow_length):len(string)]
					if(cut_str.index(end_follow)!=0):
						final_strings.remove(string_cpy)
						break
					else:
						i = i +(start_follow_length+end_follow_length)
						string = string[i:len(string)]
						
		#check one	
		strings = setofstrings
		for i in strings:
			check(i)

		#check two
		for string in final_strings:
			if(start_follow in string):
				double_check(string)

		#setting the global variable to the filtered list of strings
		setofstrings = final_strings
		return


	def alternate(self,str):

		def alternate(length, symbols):
			odd_even_pos(length,symbols,symbols[0], symbols[1])
			#doesn't matter which order you pass symbols[0], symbols[1] in
			#both cases are taken care of
			#assume the indexing is from 0
			#eg:- ababab => every even positioned char is 'a'
		def odd_even_pos(length,symbols,odd_pos_char,even_pos_char):
			#odd_pos_char = character at odd position
			#even_pos_char = char at even position	
			strings =[]
			s1=""; s2=""

			if odd_pos_char == '': #user has specified even pos character
				odd = set(symbols) - set(even_pos_char)
				for i in odd:
					odd_pos_char = i #figuring out the other character, given even positioned character and set of symbols

				for i in range(0, length+1, 2):
					s1 = s1+even_pos_char+odd_pos_char

			elif even_pos_char =='':
				even = set(symbols) - set(odd_pos_char)
				for i in even:
					even_pos_char = i #figuring out the other character, given odd positioned character and set of symbols

				for i in range(1, length+1, 2):
					s2= s2 + even_pos_char + odd_pos_char

			else:
				for i in range(0, length+1, 2):
					s1 = s1 + even_pos_char + odd_pos_char
					s2 = s2 + odd_pos_char + even_pos_char

			global setofstrings
			strings.extend((s1, s2))
			strings = [i for i in strings if i] #removing null strings

			#BACAUSE THE ALGORITHM GENERATED ONLY EVEN lengthed strings
			alternate_strings = []
			for i in strings :
				if(initiallength%2==0):
					alternate_strings.append(i[:-2])
				else:
					alternate_strings.append(i[:-1])

			# print("1",set(setofstrings))			
			# print("2",set(alternate_strings))

			setofstrings = set(setofstrings) & set(alternate_strings)



		global setofstrings
		start_alternate = str[0:str.index("$")]
		end_alternate = str[str.index("$")+1:]
		if(initiallength%2 ==0):
			initiallength_copy = initiallength -2
		else:
			initiallength_copy = initiallength - 2
		initiallength_copy = 4
		odd_even_pos(initiallength,symbols,start_alternate,end_alternate) 

	

	def divisible(self,num):
		global setofstrings
		def binaryToDecimal(n,d): 
			deci_num=int(n,2)
			if deci_num%d!=0:
				
				return False
			else:
				return True

		notdivisible = []	
		for i in setofstrings:
			if (binaryToDecimal(i,int(num)))==False:
				notdivisible.append(i)
		setofstrings = set(setofstrings)-set(notdivisible)
		
				

		

	#VERY IMPORTANT
	#FUNCTION LIST DECLARATION
	func_list  = [[0,start,""],[0,length,0],[0,end,"",],[0,even1,"",],[0,even2,"",],[0,odd1,""],[0,odd2,""]]
	secondary_func_list  = [[0,follow,""],[0,alternate,""],[0,divisible,""]]
	



	def input_spellchecker(self, entered_string):
		#INITAL STAGE OF CALLING THE SPELL CHECK
		#CHECKING OF THE CORRECTNESS OF THE INPUT
		tup = ('aa','ab','bb','ba')
		new_string = []
		#lets make a copy of entered_string
		copy_entered_string  =  entered_string[:]  #making a copy of the input
		for i in copy_entered_string.split():
			if(("'s" not in i) and ( nltk.tag.pos_tag([i])[0][1] != 'DT') and len([x for x in tup if x not in i])==4) and ("divisible" not in i) and ("atmost" not in i) and ("atleast" not in i): #obviously 4 because, for example, generate does not have any in the tuple, so len == 4, hence pass it
				new_i = spell_check.correction(i)
				new_string.append(new_i)
			else:
				new_string.append(i)
		new_entered_string  = ' '.join(new_string)

		#LET'S RETURN THIS BACK TO THE MAIN
		return new_entered_string
	
		

	def preprocessing(self,spell_checked_string):
		
		#CALLING SOME GLOBAL VARIABLES
		global atmostlength_flag
		global atleastlength_flag
		global filtered_sentence
		global error_catch
		global error_update
		global error_log
		filtered_sentence = []

		######## PREPROCESSING ! #####################
		#step 1: tokenize the string
		tokenized_words = (word_tokenize(spell_checked_string))

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
						Chunk: {<JJ><CD>}  
						Chunk: {<JJ><NN><CD>}  #atmost length 5
						Chunk: {<VBN><NN><CD>}
						Chunk: {<NN><VBD><CD>}  #length 5
						Chunk: {<RB><DT><POS>} 
						Chunk: {<JJ><NNP><POS>}
						Chunk: {<VBZ><DT><POS>}
						Chunk: {<PDT><DT><POS>}
						Chunk: {<RB><NN><POS>}
						Chunk: {<RB><VBP><POS>}
						Chunk: {<JJ><NN><POS>} ##this will select "starting with 1 (verb/preposition/cardinal number"
						Chunk: {<DT><VBN><IN><NN>} #a followed by b
						Chunk: {<NN><VBN><IN><NN>} #aa followed by b
						Chunk: {<JJ><VBN><IN><NN>} #a followed by b
						Chunk: {<NN><DT><POS><CC><NN><POS>} #alternate a's and b's
						Chunk: {<JJ><IN><CD>}
						"""   
		chunkParser  = nltk.RegexpParser(chunkGram)
		result = chunkParser.parse(tagged_words) 

		
		##THE FOLLOWING CODE RETRIEVES THE CHUNKED DATA WITHOUT THE POS TAGS
		chunked_terms = []
		for e in result.subtrees(filter=lambda t: t.label() == 'Chunk'):
			if isinstance(e, tuple):
				chunked_terms.append([ e[0] ])
			else:
				chunked_terms.append([w for w, t in e])


		print(chunked_terms)
		#Step 4: STEMMING 
		#pip install stemming==1.0 <-- used this stemmer
		do_not_stem = ("alternate","divisible") 
		for i in chunked_terms:
				k = 0
				if i[k] not in do_not_stem:
					i[k] = (stem(i[k]))


		#Step5: Removal of Stop Words and Metacharacters 
		stop_words = set(stopwords.words("english"))
		

		##ALL THE FOLLOWING IS EXCEPTION AND ERROR HANDLING
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


		#NEED TO HANDLE THE FOLLOWED BY PART AS IT HAS 3 PARAMETERS INSTEAD OF 2, HENCE WE NEED TO COMBINE AND REDUCE IT
		for i in range(len(filtered_sentence)-1):
			if(filtered_sentence[i] == "followed"):
				filtered_sentence[i+1] = filtered_sentence[i-1]+"$"+filtered_sentence[i+1]
				filtered_sentence.remove(filtered_sentence[i-1])
		for i in range(len(filtered_sentence)-2):
			if(filtered_sentence[i] == "alternate"):
				filtered_sentence[i+1] = filtered_sentence[i+1]+"$"+filtered_sentence[i+2]
				filtered_sentence.remove(filtered_sentence[i+2])

		#NOW WE NEED TO DO SOME ERROR HANDLING
		#EXAMPLE THE NUMBER OF a's cannot be odd and even at the same time
		#so basically put a simple check as follows
		exceptionfunclist = ['start','end','length']
		for i in range(0,len(filtered_sentence)-2,2):
			if(filtered_sentence[i]!=filtered_sentence[i+2] and (filtered_sentence[i] not in exceptionfunclist)): #means if the two functions are the different (example odd and even)
				#check if the parameters are the same too
				
				if(filtered_sentence[i+1]==filtered_sentence[i+2+1]) :
					error_catch.append([2,error_log[2]])  
					error_update = 1 #we update the length to keep track of its changes
					return(error_catch) #THIS RETURNS TO THE MAIN FUNCTION AGAIN WITH THE ERROR 

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

		
		#STEMMING AGAIN FOR THE LAST TIME AS FOLLOWED did not get stemmed the first time (any 3 parameter function will not get stemmed the first time)
		do_not_stem = ("alternate","divisible")
		for i in range(len(filtered_sentence)):
			if filtered_sentence[i] not in do_not_stem:
				filtered_sentence[i] = stem(filtered_sentence[i])


		print(filtered_sentence)



	#FUNCTION 1 #VERY VERY IMPORTANT	
	def initialize(self,length):

		global filtered_sentence
		global filtered_sentence_length_copy
		global count_activated_func
		global error_catch
		global error_log
		global error_update


		filtered_sentence_length_copy =  filtered_sentence[:]

		for i in range(len(filtered_sentence_length_copy)):
			if(filtered_sentence_length_copy[i]=="length"):
				filtered_sentence_length_copy[i+1] = length

		#activating the func_list
		for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
			for j in self.func_list :	
				if filtered_sentence_length_copy[i] == j[1].__name__:
					count_activated_func  = count_activated_func + 1 
					j[0] = 1
					j[2] = filtered_sentence_length_copy[i+1]	

		#SOME ERROR HANDLING
		#if count is 0, means no functions were called, hence so we catch it here itself.
		if(count_activated_func == 0):
			error_catch.append([3,error_log[3]])  
			error_update = 1 #we update the length to keep track of its changes
			return(error_catch) #THIS RETURNS TO THE MAIN FUNCTION AGAIN WITH THE ERROR 


		#UPDATE: NOW WE ARE TAKING CARE OF THE SECONDARY FUNCTION LIST TOO. THESE FUNCTIONS WILL WORK ON THE FINAL STRING GENERATED AFTER JOININ non_final_string
		#WEL WILL HAVE TO ACTIVATED THE FUNCTIONS IN THE SECONDDARY FUNCTION LIST TO
		for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
			for j in self.secondary_func_list :	
				if filtered_sentence_length_copy[i] == j[1].__name__:
					j[0] = 1
					j[2] = filtered_sentence_length_copy[i+1]	

		self.start_end_length_func()



	#FUNCTION 2
	def start_end_length_func(self):
		#LETS CALCULATE THE START LENGTH AND END LENGTH OF THE START AND END CHARACTERS
		global start_length
		global end_length
		global filtered_sentence
		global filtered_sentence_length_copy
		filtered_sentence_length_copy = filtered_sentence[:]

		for i in range(0,len(filtered_sentence_length_copy),2) : #0,2,4....going only on the function indices
			if filtered_sentence_length_copy[i]=="start":
				start_length = len(filtered_sentence_length_copy[i+1])
			if filtered_sentence_length_copy[i]=="end":
				end_length = len(filtered_sentence_length_copy[i+1])


	#FUNCTION 3 #MOST IMPORTANT FUNCTION
	def activated_function_calls(self):
		#outer order of start,end,length
		#inner order of state,function_name,parameter
		#CALLING THE FUNCTIONS USING EVAL
		#FUNCTION GETS CALLED ONLY IF STATE IS 1	
		# print(func_list)
		for i in self.func_list:   #checking if the function state is 1 and calling
			if i[0]==1:
				third_para = str(i[2])
				func_name = i[1]
				func_name(self,third_para)
				

	def secondary_activated_function_calls(self):
		#FUNCTION GETS CALLED ONLY IF STATE IS 1	
		for i in self.secondary_func_list:   #checking if the function state is 1 and calling
			if i[0]==1:
				third_para = str(i[2])
				func_name = i[1]
				func_name(self,third_para)	
		return



	#FUNCTION 4 EVEN FUNCTION
	def even(self,character):
		global string_nonfinal
		global even_odd_count
		global start_length
		global end_length
		global symbols


		#lets define some flags
		start_full = 0
		end_full = 0
		
		even_odd_count = even_odd_count + 1
		countfinal  = 0
		self.start_end_length_func()
		
		#function code begins here

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
					# return string_nonfinal #commented this out as the global variable gets affected directly
				else:
					string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
					# return string_nonfinal

			elif(start_full == 1 and end_full ==0):
				#means both start and end exist and still the number of that character is not even
				if(character in string_nonfinal[1]):
					string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
					# print("here")
					return string_nonfinal
				else:
					string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal

			elif(start_full == 0 and end_full ==1):
				#means both start and end exist and still the number of that character is not even
				if(character in string_nonfinal[1]):
					string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
					# print("here")
					# return string_nonfinal
				else:
					string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal

			elif(start_full == 0 and end_full ==0):
				#means both start and end exist and still the number of that character is not even
				if(character in string_nonfinal[0]):
					string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
					# print("here")
					# return string_nonfinal
				else:
					string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal



	def odd(self,character):

		global even_odd_count
		global string_nonfinal
		global even_odd_count
		global start_length
		global end_length

		even_odd_count = even_odd_count + 1
		countfinal  = 0
		self.start_end_length_func()
		#lets define some flags
		start_full = 0
		end_full = 0

		#main odd code begins here
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
					# return string_nonfinal
				else:
					string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal

			elif(start_full == 1 and end_full ==0):
				#means both start and end exist and still the number of that character is not even
				if(character in string_nonfinal[1]):
					string_nonfinal[1] = string_nonfinal[1].replace(character,replacement_character,1)
					# print("here")
					# return string_nonfinal
				else:
					string_nonfinal[1] = string_nonfinal[1].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal

			elif(start_full == 0 and end_full ==1):
				#means both start and end exist and still the number of that character is not even
				if(character in string_nonfinal[1]):
					string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
					# print("here")
					# return string_nonfinal
				else:
					string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal

			elif(start_full == 0 and end_full ==0):
				#means both start and end exist and still the number of that character is not even
				if(character in string_nonfinal[0]):
					string_nonfinal[0] = string_nonfinal[0].replace(character,replacement_character,1)
					# print("here")
					# return string_nonfinal
				else:
					string_nonfinal[0] = string_nonfinal[0].replace(replacement_character,character,1)
					# print("here")
					# return string_nonfinal








	#VALIDATION OF THE STRINGS GENERATED AFTER GOING THROUGH ODD AND EVEN FUNCTIONS
	def even_odd_valid(self):

		global start_length
		global end_length
		global string_nonfinal
		global even_odd_count
		global even_odd_flag
		
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
				elif(start_full == 0 and end_full == 0): #means none of them exist
					count = string_nonfinal[0].count(i[1])
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
				elif(start_full == 0 and end_full == 0): #means none of them exist
					count = string_nonfinal[0].count(i[1])
					if count%2 == 0: #means its not acutally odd
						exit_flag = 1


			#ERROR HANDLINGG
			#VERY IMPORTANT
			global error_catch
			global error_log
			global error_update
			if(exit_flag == 1):
				print("here")
				error_catch.append([4,error_log[4]])  
				error_update = 1 #we update the length to keep track of its changes
				return(error_catch)



		########################################################################################################################
		########################################################################################################################
		########################################################################################################################
		################################################# INITIALIZATION #######################################################
		########################################################################################################################
		########################################################################################################################
		########################################################################################################################


		

	def stage2_initialize(self,filtered_list):

		#CALLING GLOBAL VARIABLES
		global atmostlength_flag 
		global atleastlength_flag 
		global filtered_sentence
		global setofstrings
		global string_nonfinal
		global initiallength

		#DEFINING SOME VARIABLES
		#LETS GET THE LENGTH OF THE STRING THAT NEEDS TO BE GENERATED
		initiallength = 0
		setofstrings = [] 
		for i in range(len(filtered_sentence)):
			if(filtered_sentence[i]=="length"):
				initiallength = int(filtered_sentence[i+1])

		self.start_end_length_func() #getting the total length of the start and end characters
		total_beginlength = start_length + end_length

		##################### FINAL PRINTINTG CASE 1
		if(atmostlength_flag == 1):
			for i in range(200):
				for i in range(total_beginlength,initiallength+1):
					string_nonfinal = []

					self.initialize(i) #pass the number of characters you want to generate here

					self.activated_function_calls()

					if(even_odd_count ==2):   #means only if the function was executed twice the strings need to go through a validity check
						self.even_odd_valid()

					final_string = "".join(string_nonfinal) #joins all the strings present in the list

					setofstrings.append(final_string)

			#NOW LET'S CALL THE SECONDARY FUNCTION ACTIVATOR AND ACTIVATED THE SECONDARY FUNCTIONS
			self.secondary_activated_function_calls()		
			setofstrings = set(setofstrings)
			setofstrings = sorted(setofstrings, key=len)



		##################### FINAL PRINTING CASE 2

		if(atleastlength_flag == 1):
			
			for i in range(200):
				for i in range(initiallength,initiallength + 3): #10 is a random number
					string_nonfinal = []
					self.initialize(i) #pass the number of characters you want to generate here
					self.activated_function_calls()

					if(even_odd_count ==2):
						self.even_odd_valid()

					
					final_string = "".join(string_nonfinal) #joins all the strings present in the list
					
					setofstrings.append(final_string)

			#NOW LET'S CALL THE SECONDARY FUNCTION ACTIVATOR AND ACTIVATED THE SECONDARY FUNCTIONS
			self.secondary_activated_function_calls()

			setofstrings = set(setofstrings)
			setofstrings = sorted(setofstrings, key=len)
			


		#means if those particular set of codes were executed, don't execute the others
		if(atmostlength_flag == 1 or atleastlength_flag == 1):

			#VERY IMPORTANT RETURN 
			return setofstrings  #RETURNING TO THE GUI
			exit()


		##################### FINAL PRINTINTG CASE 3

		setofstrings = [] 
		for i in range(200):
			string_nonfinal = []
			self.initialize(initiallength) #pass the number of characters you want to generate here

			#if an error occurs in the initialize function
			if(error_update==1):
				return(error_catch)


			self.activated_function_calls()

			if(even_odd_count ==2):
				self.even_odd_valid()
			final_string = "".join(string_nonfinal) #joins all the strings present in the list
			setofstrings.append(final_string)  #prints out the final string

		#NOW LET'S CALL THE SECONDARY FUNCTION ACTIVATOR AND ACTIVATED THE SECONDARY FUNCTIONS
		self.secondary_activated_function_calls()


		setofstrings = set(setofstrings)
		setofstrings = sorted(setofstrings, key=len)
		return setofstrings #RETURNING TO THE GUI


obj = test_class()
# # print(obj.input("Generate a string starting with a and ending with b and having length 4"))
# result = obj.input("Generate a string having length as 5 with alternate a's and b's")
# print(type(result))


result  = obj.input("Generate a string having length atmost 4 and starting with b")
print(result)
# print(type(error_catch))

f = open("input.txt",'w')
for i in result[1]:
	f.write(i+"\n")

