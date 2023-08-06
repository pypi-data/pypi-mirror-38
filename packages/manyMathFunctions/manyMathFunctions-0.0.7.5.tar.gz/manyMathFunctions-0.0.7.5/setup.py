from setuptools import setup, find_packages

desc = open('readme.md', 'r')

setup(
    name="manyMathFunctions",
    version="0.0.7.5",
    author="TheOnlyWalrus",
    description="See long description / README.md",
    long_description=desc.read(),
    long_description_content_type="text/markdown",
    url="https://manymathfunctions.readthedocs.io/en/latest/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Natural Language :: English",
    ],
)