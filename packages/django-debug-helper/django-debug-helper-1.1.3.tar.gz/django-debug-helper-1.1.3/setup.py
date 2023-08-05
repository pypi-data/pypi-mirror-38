import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-debug-helper",
    version="1.1.3",
    author="Mohd. Shafikur Rahman",
    author_email="shafikshaon@gmail.com",
    description="Django debug error related exception search on Google/ Stack Overflow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shafikshaon/django-debug-helper",
    packages=['django-debug-helper'],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
    ],
)