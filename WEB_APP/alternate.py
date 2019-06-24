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

	strings.extend((s1, s2))
	strings = [i for i in strings if i] #removing null strings
	print(strings)

odd_even_pos(6-2, ['a', 'b'], 'a', 'b') 
alternate