# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(name='wanghongyan',
	version='0.4',
	description='',
	author='wanghongyan',
	author_email='258156979@qq.com',
	install_requires=[],
	packages=['bin'],
	package_data={
		'bin':['*.sh']
	},
	include_package_data=True,
	zip_safe=False,
	url='https://github.com/258156979/wanghongyan',
	keywords=''
)
#packages=find_packages(),
