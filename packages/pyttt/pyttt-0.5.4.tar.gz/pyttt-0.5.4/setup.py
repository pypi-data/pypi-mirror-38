from setuptools import setup,find_packages
with open("README.md",encoding='utf-8') as f:
	long_desc=f.read()
setup(
name='pyttt',
version='0.5.4',
description='Multi Player Tic Tac Toe Game',
long_description=long_desc,
long_description_content_type="text/markdown",
url="https://github.com/CKVB/Tic-Tac-Toe/blob/master/ttt.py",
author='Chaitanya Krishna VB',
author_email='python7460@gmail.com',
license='MIT LICENSE',
packages=find_packages(),
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)