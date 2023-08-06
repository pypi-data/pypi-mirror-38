'''
用于打印多重嵌套列表元素的函数
'''
def func1(st):
        # 循环查询列表元素，找出其中的属于列表的元素
	for each_st in st:
		if isinstance(each_st,list):
			func2(each_st)
		else:
			print(each_st)
