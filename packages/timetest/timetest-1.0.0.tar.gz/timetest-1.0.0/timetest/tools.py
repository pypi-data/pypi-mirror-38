import time


def alltime_test(func=None, count=10, *args, **kwargs):
	times = []
	
	if str(type(func)) != "<class 'function'>":
		print(str(func) + " is not a function!")
		
	for i in range(count):
		start_time = time.time()
		func(*args, **kwargs)
		
		times.append(time.time() - start_time)
		
	return times


def averagetime_test(func=None, count=10, *args, **kwargs):
	summ = 0
	for t in alltime_test(func, count, *args, **kwargs):
		summ += t
	
	return(summ/count)


