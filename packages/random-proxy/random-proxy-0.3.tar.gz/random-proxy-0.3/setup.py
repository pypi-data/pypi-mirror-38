#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
	name='random-proxy',
	version='0.3',
	keywords=("random proxy", "spider random proxy"),
	description=(
		'Generate a random proxy and return a tuple containes IP and Port.'
	),
	author='kuing',
	author_email='samleeforme@gmail.com',
	packages=find_packages(),
	license='MIT',
	url="https://github.com/kuingsamlee/weiboCommentCrawl/blob/master/random_proxy.py",
	platforms=['all']
)

