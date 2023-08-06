'''
Contains informations necessaries to build, release and install a distribution.
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='py-sqlite-orm-danidr',
    version='0.0.1',
    author='danydr',
    author_email='ddv_2010@mail.ru',
    url='https://github.com/DruzhininDV/sqlite-orm',
    description='A Python object relational mapper for SQLite.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['orm'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]  # see more at https://pypi.python.org/pypi?%3Aaction=list_classifiers
)
