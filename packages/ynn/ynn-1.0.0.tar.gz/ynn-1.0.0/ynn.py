'''这个函数用于打印列表中的列表
支持多层嵌套打印，使用方便
欢迎大家修改和改进，ynngood163.com '''
def print_lol(the_list):
    for item in the_list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)
cast = [1,2,3,[4,5,6,[7,8,9,[10,11,12]]],13,14,15]
print_lol(cast)
