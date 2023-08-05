#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/11/5 17:56
# software:PyCharm
from .programs import C, Common, CSharp, Cpp, JavaScript, Python, Php, Assembly, Java, Shell, Go, program
import random


def faker(k=1, name_list=[]):
    if k > 0:
        name_list.extend(random.choice(list(program.values())).faker())
        faker(k=k-1, name_list=name_list)
    return name_list
