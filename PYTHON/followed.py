import re
 # strings =  ['bbbba', 'babaa', 'bbaba', 'babab', 'bbaab', 'abbab', 'baabb', 'babba', 'aabbb', 'babbb', 'aaaba', 'abaaa', 'aaaab', 'bbaaa', 'aaabb', 'aabab', 'ababb', 'abbbb', 'bbabb', 'abaab', 'aaaaa', 'ababa', 'baaaa', 'abbaa', 'baaba', 'bbbab', 'baaab', 'aabaa', 'bbbbb', 'aabba']
strings = ['bbaabb', 'bbbabb','abb','abbabb']
allowed = []

for i in strings:
	strings_main=[]
	strings_main.append(i)
	indexlist = []

	start = 'aa'
	follow = 'bb'

	tofind = start+follow

	strings_copy = []
	for i in strings_main:
		pos = [m.start() for m in re.finditer(tofind,i)]
		if(pos!=[]):
			strings_copy.append(i)
			indexlist.append(pos)

	total_pattern_len = len(tofind)

	
	for i in indexlist:
		no_of_start = 0 #just initialising

		if(len(i) == 1):
			if(i[0]!=0):
				len_of_string = len(strings_copy[indexlist.index(i)])

				no_of_start = strings_copy[indexlist.index(i)][0:i[0]].count(start)

				no_of_start = no_of_start + strings_copy[indexlist.index(i)][i[0]+len(tofind):len_of_string].count(start)

				if(no_of_start==0):
					allowed.append(strings_copy[indexlist.index(i)])

			if(i[0]==0):
				# print("here")
				len_of_string = len(strings_copy[indexlist.index(i)])
				# print(len_of_string)
				no_of_start = no_of_start + strings_copy[indexlist.index(i)][i[0]+len(tofind):len_of_string].count(start)
				# print(no_of_start)
				if(no_of_start==0):
					allowed.append(strings_copy[indexlist.index(i)])
					
		else:
			num = 0
			for k in range(0,len(i)):
					if(i[k] != i[-1]):

						num = num + strings_copy[indexlist.index(i)][i[k]:i[k+1]].count(start)
					else:
						num = num + strings_copy[indexlist.index(i)][i[k]:].count(start)


			if(num == len(i)):
				allowed.append(strings_copy[indexlist.index(i)])

print(allowed)

# iterlen = len(indexlist)
# diff = []
# for j in indexlist:
# 	diff.append([m-n for n, m in zip(j[:-1], j[1:])])


# print(diff)




		# if(j==0):
		# 	remain_len = total_pattern_len - indexlist[i]
		# 	for i in range(remain_len,total_pattern_len):







