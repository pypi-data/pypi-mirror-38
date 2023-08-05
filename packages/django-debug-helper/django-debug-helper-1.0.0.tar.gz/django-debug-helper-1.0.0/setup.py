import setuptools
from distutils.core import setup


setuptools.setup(
    name="django-debug-helper",
    version="1.0.0",
    author="Mohd. Shafikur Rahman",
    author_email="shafikshaon@gmail.com",
    description="Django debug error related exception search on Google/ Stack Overflow.",
    url="https://github.com/shafikshaon/django-debug-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)