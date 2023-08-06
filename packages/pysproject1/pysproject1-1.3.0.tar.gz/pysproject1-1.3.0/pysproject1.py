import sys
'''
用于打印多重嵌套列表元素的函数
'''
def func1(st,isneed=False,level=0,fh=sys.stdout):
        # 循环查询列表元素，找出其中的属于列表的元素
        for each_st in st:
                if isinstance(each_st,list):
                        func1(each_st,isneed,level+1,fh)
                else:
                        #打印指定的缩进
                        if isneed:
                                for i in range(level):
                                        print("\t",end='',file=fh)
                        print(each_st,file=fh)

			
