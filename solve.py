def solution(A, S):
	count = 0
	# print(len(A))
	for i in range(len(A)):
		summation = 0
		for j in range(len(A) - i):
			sumValue = sum(A[j:(j+i+1)])
			print(i+1, A[j:(j+i+1)], sumValue)
			if(sumValue % (i+1) == 0):
				average = int(sumValue / (i+1))
				print(i+1, A[j:(j+i+1)], sumValue, average)
				if(average == S):
					count = count + 1
	return count

a = solution([2,1,4], 3)
print(a)