import numpy as np
import random


def multiply(x, y):
	x_bits = 11
	y_bits = 11
	length = x_bits + y_bits +1
	x_binary = np.binary_repr(x, x_bits)  # convert x to binary
	y_binary = np.binary_repr(y, y_bits)  # convert y to binary
	neg_x_binary = np.binary_repr(-1*x, x_bits)  # convert -x to binary
	# print("x", x_binary, "-x", neg_x_binary, 'y', y_binary)
	y_zero_string = ''
	x_zero_string = ''
	for i in range(0, y_bits+1):
		y_zero_string += '0'
	for i in range(0, x_bits):
		x_zero_string += '0'
	A = x_binary + y_zero_string  # A = x_binary + (y_bits + 1) 0
	S = neg_x_binary + y_zero_string  # S = negative_x_binary + (y_bits + 1) 0
	P = x_zero_string + y_binary + '0'  # P = (x_bits) 0 + y_binary + 0
	# print("A", A, "S", S, "P", P)
	count = 0

	while(count < y_bits):
		# print("count", count)
		righ_bits_P = P[-2:]  # find rightmost 2 bits of P

		if(righ_bits_P == "01"):  
			sum_val_decimal = int(P,2) + int(A,2)  # add P and A in decimal form
			# print('P={}'.format(P))
			# print('A={}'.format(A))
			# print('sum_val_decimal={}'.format(sum_val_decimal)) 
			sum_val = np.binary_repr(sum_val_decimal, length)  # convert back to binary
			# print('sum_val={}'.format(sum_val))

		elif(righ_bits_P == '10'):
			sum_val_decimal = int(P,2) + int(S,2)  # add P and S in decimal form
			# print('P={}'.format(P))
			# print('S={}'.format(S))
			# print('sum_val_decimal={}'.format(sum_val_decimal))
			sum_val = np.binary_repr(sum_val_decimal, length)  # convert back to binary
			# print('sum_val={}'.format(sum_val))

		else:  # if rightmost bits are 00 or 11
			sum_val = P
		# print("sum_val", sum_val)
		sum_val = sum_val[-1*length:]

		if(sum_val[0] == '1'): 
			P = '1' + sum_val[:-1]  # rightward shift of P
		if(sum_val[0] == '0'):
			P = '0' + sum_val[:-1]  # rightward shift of P
		# print("P", P)
		count += 1

	ans_binary = P[:-1]  # remove the rightmost bit in P
	temp = ''
	neg = False
	if(ans_binary[0] == '1'):  # if most significant bit is 1 then answer is negative
		neg = True
		for i in range(len(ans_binary)):
			if(ans_binary[i] == '1'):
				temp += '0'
			if(ans_binary[i] == '0'):
				temp += '1'
		ans_decimal = int(temp, 2) + 1
		ans_decimal = -1 * ans_decimal
	else:
		ans_decimal = int(ans_binary, 2)  # else answer is positive
	return ans_binary, ans_decimal


def subtract(Rem, div):
	Ans = []
	C = 0
	for j in range(len(Rem)):
		i = len(Rem) - 1 - j;
		A = int(Rem[i])
		B = int(div[i]);
		Ans = [str((A^B)^C)] + Ans
		C = (A^1)*(B or C) or (B*C)
	# print(ToString(Ans))
	return Ans


def ToString(Arr):
	ans = ''
	for i in Arr:
		ans += i
	return ans


def RestoreDivision(dividend, divisor):

	case = 0

	if(dividend > 0 and divisor<0):
		case = 1
	if(dividend < 0 and divisor > 0):
		case = 2
	if(dividend < 0 and divisor < 0):
		case = 3

	divisor = abs(divisor)
	dividend = abs(dividend)

	if divisor > dividend:
		Quotient = 0
		Remainder = dividend

	else:
		# Restoring Algo
		# Div is the divisor register
		# Rem is the remainder register
		# Quo is the Quotient register 
		# Restore is the register that stores restoration bit


		# Step 1 - Initializing values
		Div = [i for i in format(divisor, "b")];
		Quo = [i for i in format(dividend, "b")];
		n = len(Quo);
		Rem = ["0"]
		for i in range(n):
			Rem+=["0"];
		for i in range(n - len(Div) + 1):
			Div = ["0"] + Div;
		Restore = 0
		# print(n, ToString(Div), ToString(Rem), ToString(Quo), Restore)


		#Algo start
		while n  > 0:
			# Shift remainder left
			for i in range(len(Rem) - 1):
				Rem[i] = Rem[i+1]
			Rem[len(Rem) - 1] = Quo[0]

			# Subracting Divisor from Remainder
			PossibleRem = subtract(Rem, Div)
			if PossibleRem[0] == '1':
				Restore = 0
			else:
				Restore = 1
				Rem = PossibleRem

			# Shifting quotient while restoring the last bit
			for i in range(len(Quo) - 1):
				Quo[i] = Quo[i+1]
			Quo[len(Quo) - 1] = str(Restore)
			# print(n, ToString(Div), ToString(Rem), ToString(Quo), Restore)

			n -= 1

		Remainder = ''
		Quotient = ''
		for i in Rem:
			Remainder += i

		for i in Quo:
			Quotient += i

		# Converting back to decimal
		Quotient = int(Quotient, 2)
		Remainder = int(Remainder, 2)

	# Checking for negative numbers explicitly
	if(case == 1 ):
		Quotient = (-1)*Quotient
		if(Remainder != 0):
			Quotient -= 1
			Remainder -= divisor
	if(case == 2):
		Quotient = (-1)*Quotient
		if(Remainder != 0):
			Quotient -= 1
			Remainder = (-1)*Remainder + divisor
	if(case == 3):
		Remainder = (-1)*Remainder 

	return (Quotient, Remainder)



if __name__ == '__main__':
	
	OutputFile = open("Output.txt", 'a')
	print("Enter 1 to multiply and 2 to divide")
	choice = int(input())
	if(choice == 1):

		print("Enter numbers to be multiplied")
		x = int(input())  
		y = int(input())
		ans_binary, ans_decimal = multiply(x,y)
		print("Binary answer: ", ans_binary)
		print("Decimal answer ", ans_decimal)
		OutputFile.write(str(x)+" X "+str(y)+ " = " + str(ans_decimal)+" ")
		OutputFile.write("Binary Answer = " + ans_binary+"\n")


	else:
		passed = True
		print("Enter the value of dividend and enter")
		try:
			dividend = int(input());
		except:
			print("Not a valid dividend")
			passed = False
		print("Enter the value of divisor and enter")
		try:
			divisor = int(input());
		except:
			print("Not a valid divisor")
			passed = False

		if divisor == 0:
			OutputFile.write("Dividend = "+str(dividend)+" Divisor = "+str(divisor)+"\n")
			OutputFile.write("ERROR : Division by 0 \n")
			print("ERROR : Division by 0 ")
		elif passed != False:
			Quotient, Remainder = RestoreDivision(dividend, divisor);
			OutputFile.write("Dividend = "+str(dividend)+" Divisor = "+str(divisor))
			print("Quotient is ", Quotient)
			print("Remainder is ", Remainder)
			OutputFile.write(" Quotient = " + str(Quotient) + " Remainder = "+ str(Remainder) + "\n")