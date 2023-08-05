from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='WatsonReport',
    author="Kobe De Decker",
    author_email="kobededecker@gmail.com",
    description="watson reporting for imdc",
    version='0.0.3',
    packages=find_packages(),
    install_requires=['pandas', 'subprocess', 'shlex', 'json', 'watson'],
    url="https://gitlab.com/kobededecker/watsonreport",
    scripts=[r".\scripts\watsonreport.bat", r".\scripts\watsonreport.py"],
    license='MIT',
)