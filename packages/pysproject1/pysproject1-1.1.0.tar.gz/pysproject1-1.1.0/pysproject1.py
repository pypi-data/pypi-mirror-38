'''
用于打印多重嵌套列表元素的函数
'''
def func1(st,level):
        # 循环查询列表元素，找出其中的属于列表的元素
        for each_st in st:
                if isinstance(each_st,list):
                        func1(each_st,level+1)
                else:
                        #打印指定的缩进
                        for i in range(level):
                                print("\t",end='')
                        print(each_st)
			
