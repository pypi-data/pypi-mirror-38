
from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "Taobao-Spider",      #这里是pip项目发布的名称
    version = "1.0.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "Taobao"," spider","淘宝","爬虫"),
    description = "A spider of taobaogoods",
    long_description = "A spider of taobaogoods",
    license = "MIT Licence",

    url = "https://github.com/xjkj123/Taobao-Spider",     #项目相关文件地址，一般是github
    author = "MRX",
    author_email = "xjkj123@icloud.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests', 'pandas', 'tqdm']
)

