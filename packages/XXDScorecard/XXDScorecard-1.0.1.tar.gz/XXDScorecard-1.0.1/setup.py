# -*- coding: utf-8 -*-
PACKAGE = "XXDScorecard"
NAME = "XXDScorecard"
DESCRIPTION = "scorecard developing utilities."
AUTHOR = "徐小东(xxd626@outlook.com) and 郁晴(873237045@qq.com)"
AUTHOR_EMAIL = "xxd626@outlook.com"
URL = "https://github.com/xxd626"
VERSION = '1.0.1'

from setuptools import setup, find_packages

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
	keywords = ("woe", "iv","binning", "scorecard"),
    long_description="""

用于数值型和字符型变量的分箱类。
支持手动分箱，等频分箱，单调分箱，IV、WOE计算及转换。

@author: 徐小东(xxd626@outlook.com) and 郁晴(873237045@qq.com)
@date: new_version on 2018/11/3
""",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL, packages = find_packages(),
    include_package_data = True
     
)