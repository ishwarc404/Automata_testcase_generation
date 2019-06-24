
start_follow = 'aa'
end_follow = 'bb'
start_follow_length = len(start_follow)
end_follow_length = len(end_follow)
final_strings=[]
def check(string):
	count_start_end = string.count(start_follow+end_follow)
	count_start = string.count(start_follow)
	if(count_start_end== count_start):
		final_strings.append(string)


strings = ['bbaabb', 'bbbabb','abb','abbabb']
for i in strings:
	check(i)

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
				
		#print(i)
		#i= i+1
print("1. Final Strings:", final_strings)

for string in final_strings:
	if(start_follow in string):
		
		double_check(string)


print(final_strings)