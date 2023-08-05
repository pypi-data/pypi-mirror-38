# xxprogram
这是一个随机名称生成器，使用程序员相关的梗，可用于生成若干用户名（有重复可能），eg:   
```
IN[1]:  import XXProgram as P
        P.Python.faker(k=3)
OUT[1]:  ['自带游标卡尺的Python程序员', 
         '不会修电脑的Python程序员', 
         'import 别人的程序的Python程序员']
IN[2]:  P.faker(k=3)
OUT[2]:  ['0 Error 0 Warning的程序员',
         'IT界首屈一指的的C++程序员',
         '不写文档的Shell程序员']
```
## 安装
```commandline
pip install xxprogram
```
或
```commandline
cd xxprogram
python setup.py install
```