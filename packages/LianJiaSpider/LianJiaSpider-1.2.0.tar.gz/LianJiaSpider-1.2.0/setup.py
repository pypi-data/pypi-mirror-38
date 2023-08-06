#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="LianJiaSpider",  # 这里是pip项目发布的名称
    version="1.2.0",  # 版本号，数值大的会优先被pip
    keywords=("pip", "LianJiaSpider", "API","链家"),
    description="An self made api for lianjia",
    long_description="链家API可以实现区域找小区，小区找房接口，接口无限制，适合大量数据分析",
    license="GNU Licence",

    url="https://github.com/xjkj123/Lianjia/",  # 项目相关文件地址，一般是github
    author="Mrx",
    author_email="xjkj123@icloud.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy","requests","tqdm"]  # 这个项目需要的第三方库
)
