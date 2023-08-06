from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='twill3',
    version='0.11.2',
    scripts=['twill'],
    packages=find_packages(),
    author='Jon Froiland',
    author_email='jon.froiland@gmail.com',
    description='Update twill for Python3 compatibility',
    long_description='Using 2to3, refactored code for Python3. Version references <version>.<month>.<change>',
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ], install_requires=['lxml', 'requests', 'pyparsing']
)
