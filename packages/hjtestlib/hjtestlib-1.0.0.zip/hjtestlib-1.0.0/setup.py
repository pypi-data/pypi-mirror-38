from setuptools import setup

def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
          return rf.read()

setup(name="hjtestlib", version="1.0.0", description="this is a hj lib",
      packages=["hjtestlib"], py_modules=["Tool"], author="Hj", author_email="1573786811@qq.com",
      long_description=readme_file(), url="https://www.baidu.com", license="MIT")