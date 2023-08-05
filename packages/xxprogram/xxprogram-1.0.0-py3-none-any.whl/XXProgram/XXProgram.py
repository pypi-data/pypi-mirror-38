#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/11/4 20:28
# software:PyCharm
import random


"""
这是一个随机名称生成器，使用程序员相关的梗，可用于生成若干用户名（有重复可能），eg: 
IN[1]:  import XXProgram as P
        P.Python.faker(k=3)
OUT[1]:  ['自带游标卡尺的Python程序员', '不会修电脑的Python程序员', 'import 别人的程序的Python程序员']
"""


class Common(list):
    """
    通用类，格式为xx的程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "第0名", "第1024名", "写文档", "看文档", "怀疑自己", "加班", "写注释", "不写注释", "开源死亡产品",
            "不写文档", "痛骂别人不写文档", "痛骂别人不写注释", "写API", "说谎：//TODO", "不喜欢当码农", "没有头发",
            "离开电脑是废物", "有强迫症", "Control+S", "Hello World", "0 Error 0 Warning", "不喜欢八阿哥",
            "从入门到放弃", "改需求", "不会修电脑", "Control+C,ControlV"
        ])

    @classmethod
    def faker(cls, k=1, common=True):
        """
        :param k:默认为1
        :return: 字符串列表，根据类的不同返回格式为xx的xx程序员或xx的程序员
        """
        i = list(filter(lambda x: program[x] == cls, program.keys()))[0]
        if i == 'Common':
            return list(map(lambda x: '{}的程序员'.format(x), random.choices(cls(), k=k)))
        else:
            return list(map(lambda x: '{}的{}程序员'.format(x, i), random.choices(cls(), k=k)))


class Python(Common):
    """
    Python类，格式为xx的Python程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "import 别人的程序", "多打了一个空格", "喜欢蝙蝠侠", "手持双管枪", "好久不见", "人文主义", "玩蛇", "重生",
            "学习大数据和人工智能", "动态类型", "强类型", "自带游标卡尺", "最易学习", "又是GIL!", "用Django", "用PIL",
            "当黑客", "用Flask",

        ])


class Java(Common):
    """
    Java类，格式为xx的Java程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "读完两页不知道作用", "喜欢万磁王", "开大众", "手持M240自动机枪", "不是JavaScript爹", "从银行拿钱",
            "活泼，努力", "信仰基督教", "玩积木", "掌握大权", "写安卓应用", "用SpringMVC", "等待启动", "培训中",
            "看不起C#程序员"
        ])


class C(Common):
    """
    C语言类，格式为xx的C程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "忘了添加null终止符", "开林肯", "手持加兰德步枪", "万物起源", "信仰犹太教", "造积木", "有深入洞察力",
            "第一个吃螃蟹", "面向过程", "写操作系统", "看不起Java程序员"
        ])


class Shell(Common):
    """
    Shell类，格式为xx的Shell程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "没有足够的权限", "输入rm -rf", "询问第二次"
        ])


class Cpp(Common):
    """
    C++类，格式为xx的C++程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "复制了四百次",  "喜欢机械战警", "开捷豹", "手持双截棍", "能赚大钱", "IT界首屈一指的", "信仰伊斯兰教",
            "比C更有野心", "面向对象", "最复杂", "开发嵌入式", "看不起C程序员"
        ])


class Php(Common):
    """
    PHP类，格式为xx的PHP程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "我只看到钱", "喜欢小丑", "开五菱宏光",  "排气管接进车窗", "Web世界机器人", "信仰基督教", "世界上最好",
            "开发Web", "不接受反驳"
        ])


class Assembly(Common):
    """
    汇编类，格式为xx的汇编程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "喜欢绿巨人", "只会助记符"
        ])


class CSharp(Common):
    """
    C#类，格式为xx的C#程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "开众泰", "架在驴子上的大炮", "信任微软", "IT界最强", "信仰摩门教", "借鉴Java", "自称不是Java",
            "开发Unity3D", "全面集成.NET", "//", "看不起美工"
        ])


class JavaScript(Common):
    """
    JavaScript类，格式为xx的JavaScript程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "开特斯拉", "手持宝剑", "不是Java儿子", "面无表情", "非常受欢迎", "最长寿", "不是Java", "动态类型",
            "弱类型", "不是Java分支", "运行在客户端", "想成为全栈工程师", "兼容IE6", "开发前端", "同时开发后端",
            "同时开发Android和IOS", "开发小程序", "false/null/NaN/undefined"
        ])


class Go(Common):
    """
    Go类，格式为xx的Go程序员
    """
    def __init__(self):
        super().__init__()
        self.extend([
            "发射发令枪", "出身名门", "面向未来"
        ])


program = {
    'Python': Python,
    "Go": Go,
    'Javascript': JavaScript,
    'C++': Cpp,
    '汇编': Assembly,
    'C#': CSharp,
    "PHP": Php,
    'Java': Java,
    'Shell': Shell,
    'C': C,
    "Common": Common,
}