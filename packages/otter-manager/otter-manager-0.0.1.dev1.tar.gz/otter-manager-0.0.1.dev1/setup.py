from codecs import open
from setuptools import setup, find_packages

with open('pypi-content.rst', encoding='utf-8') as f:
    README = f.read()

with open('otter/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if '__version__' in line:
            version = line.split("'")[1]

setup(
    name='otter-manager',
    version=version,
    description="A cli tool to manage python application more simply.",
    install_requires=[
    ],
    long_description=README,
    url='https://github.com/JeongUkJae/otter',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities"
    ],
    entry_points={
    },
    packages=find_packages(exclude=['tests'])
)
