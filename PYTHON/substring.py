########
#REMEMBER ::: WE NEED TO EDIT THE FINAL LENGTH FUNC GENERATED STRING BASED ON START AND END IF EVEN OR ODD IS CALLED
########
def length(y):
	y = int(y)
	y  = y - int(start_length) - int(end_length) #obviously
	
	#symbol loop
	# sym = ""
	# for i in symbols:
	# 	y  = y - len(i)
	

	#case1:when total length of a symbol is greater than the middle length
	symbols_copy = symbols
	for i in symbols_copy :
		if len(i) > y :
			symbols_copy.remove(i)  #this means now the random string will not consist of that string coz it cannot fit

	#print(symbols_copy)

	#case2 : when the length of the remaining symbols is the same
	len_list = [] #list of the lengths of all the symbols
	for i in symbols_copy:
		len_list.append(len(i))

	#checking if length is same
	sum  = 0
	for i in len_list:
		sum = sum + i


	if(len_list[0]== sum/len(len_list)): #print("same lengthed symbols")

		#if length of middle part is even and length of symbols is same &&& length of middle is divisible by sym
		if(y%2==0 and ((y%len_list[0])==0)):
			y = int(y/len_list[0])   #y divided by any length coz all the same # wont work if y is odd
			randomstr = ''.join([np.random.choice(symbols) for n in range(y)]) 
			string_nonfinal.append(randomstr)
			return

		#if length of middle part is even and length of symbols is same &&& length of middle is NOT divisible by sym
		if(y%2==0 and ((y%len_list[0])!=0)):
			print("NOT POSSIBLE TO GENERATE MIDDLE STRING WITH THAT COMBO")
			return

		else:
			print("NOT POSSIBLE TO GENERATE MIDDLE STRING WITH THAT COMBO")
			print("LENGTH OF STRING CANNOT BE ODD and length of boths symbols cannot be same simulataneously")
			return


		
	else:
		print("not same lengths")
		return
		#need to do something else