movies = [
            "The Holy Grail", 1975,
            "The Life of Brian", 1979,
            "The Meaning of Life", 1983,
             "Graham Chapman", ["Michael Palin","John Cleese","Terry Gilliam","Eric Idele","Terry Jones"]
          ]

# 函数递归，py 3 默认为递归深度不能超过 100
"""
这是nester.py模块，提供了一个名为print_lol()的函数。
这个函数的作用是打印列表，其中有可能包含（也有可能不包含）嵌套列表
这个函数取一个位置参数名为the_list, 这可以是任何python列表(也可以是包含嵌套列表的列表）。
所指定的列表中的每个数据项会（递归地）输出到买进上，各数据项各占一行。
"""
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

# print_lol(movies)