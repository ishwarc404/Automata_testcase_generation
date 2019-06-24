'''
ERROR HANDLING DONE :
1. single characters are also a part of stop words. hence starting with 'a' , the a gets removed. hence we initialize the list of alphabets
and filter the stop words from that.
'''

#############

import nltk
from nltk.tokenize import word_tokenize #to tokenize
from nltk.corpus import stopwords #to remove the stop words
from stemming.porter2 import stem #for stemming

import string #for a list of all the alphabets


string = "Generate a string starting with a and ending with b having length 9  with even a's and even b's"

#need to follow phrase structure rules
#parse tree

######## PREPROCESSING ! #####################

#step 1: tokenize the string
tokenized_words = (word_tokenize(string))

#print(tokenized_words)
#step 2: we need to eliminate the stop words
"""One of the first steps to pre-processing is to utilize stop-words. 
Stop words are words that you want to filter out of any analysis. 
These are words that carry no meaning, or carry conflicting meanings 
that you simply do not want to deal with. """


#step3 ? need to stem or not ?



#step 4 SPEECH TAGGING 
#lets use tokenized word list to process or else we can use the PunktSentenceTokenizer and train it and use it agai
#and then re-tokenize using word_tokenize 


tagged_words = nltk.pos_tag(tokenized_words)
print(tagged_words)


## this tells which category of speech do each of those words belong to


##step 5 : chunking. basically grouping together the tokenized words to form bigger chunks
##lets run a chunk parser to understand
chunkGram = r"""Chunk: {<VBG><IN><CD>}    ##EACH OF THESE CHUNKERS WERE DECIDED BY TRIAL AND ERROR METHOD
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
				Chunk: {<JJ><NN><POS>} """   ##this will select "starting with 1 (verb/preposition/cardinal number"
chunkParser  = nltk.RegexpParser(chunkGram)
result = chunkParser.parse(tagged_words) 
#print(type(result))


# result.draw()  #gives a visual representation of the chunked parse tree



##THE FOLLOWING CODE RETRIEVES THE CHUNKED DATA WITHOUT THE POS TAGS
chunked_terms = []
for e in result.subtrees(filter=lambda t: t.label() == 'Chunk'):
   if isinstance(e, tuple):
   	chunked_terms.append([ e[0] ])
   else:
    chunked_terms.append([w for w, t in e])

#print(chunked_terms)


##STEMMING 
#pip install stemming==1.0 <-- used this stemmer
for i in chunked_terms:
	k = 0
	i[k] = (stem(i[k]))
print(chunked_terms)   ##this gives a list of list of all the stemmed terms


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



#REMOVING THE 's and shit metacharacters
for i in filtered_sentence:    
	if i == "'s":
		filtered_sentence.remove("'s")

#print(filtered_sentence) #now this is a list not containing all the stop words


#NEED TO HANDLE "ATLEAST" and "ATMOST" KEYWORD HERE ITSELF OR ELSE THE NEXT LOOP WILL GIVE ERROR
atleastlength_flag = 0
if "atleast" in filtered_sentence:
	filtered_sentence.remove("atleast")
	atleastlength_flag = 1

atmostlength_flag = 0
if "atmost" in filtered_sentence:
	filtered_sentence.remove("atmost")
	atmostlength_flag = 1


#NOW WE NEED TO DO SOME ERROR HANDLING
#EXAMPLE THE NUMBER OF a's cannot be odd and even at the same time
#so basically put a simple check as follows
exceptionfunclist = ['start','end','length']
for i in range(0,len(filtered_sentence)-2,2):
	if(filtered_sentence[i]!=filtered_sentence[i+2] and (filtered_sentence[i] not in exceptionfunclist)): #means if the two functions are the different (example odd and even)
		#check if the parameters are the same too
		if(filtered_sentence[i+1]==filtered_sentence[i+2+1]) :
			print("ERR0R: The same character cannot have both even and odd numbered occurances")

	elif(filtered_sentence[i]==filtered_sentence[i+2]): #removing multiple occurances of the same function
		if(filtered_sentence[i+1]==filtered_sentence[i+2+1]):
			print(filtered_sentence)
			filtered_sentence.pop(i+2)
			filtered_sentence.pop(i+2)

print(filtered_sentence)


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

