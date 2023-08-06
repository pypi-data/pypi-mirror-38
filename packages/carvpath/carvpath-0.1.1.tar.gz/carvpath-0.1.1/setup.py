from setuptools import setup, find_packages
from os import path

setup(
    name='carvpath',
    version='0.1.1',
    description='CarvPath designations library',
    long_description="""A simple library for using and manipulating CarvPath designations.

    Python library for manipulating MattockFS/CarvFS style CarvPath data archive designations.
    """,
    url='https://github.com/pibara-utopian/pycarvpath',
    author='Rob J Meijer',
    author_email='pibara@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Environment :: Other Environment',
    ],
    keywords='forensics carvpath',
    packages=find_packages(),
)

