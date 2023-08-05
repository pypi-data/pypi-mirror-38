import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='xxprogram',
    version='1.1.0',
    py_modules=['XXProgram'],
    author='ZRui',
    description='用程序员梗随机生成用户名',
    author_email='a1571093237@msn.cn',
    url='https://github.com/zhonlaoda/xxprogram',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)