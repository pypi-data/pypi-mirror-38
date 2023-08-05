from setuptools import find_packages, setup


setup(
    name='eetv',
    version='0.0.2',
    license='GPL3',
    description='Python bindings for the EETV appliance',
    long_description=open('README.rst').read(),
    author='Kev Swindells',
    author_email='kjs@kjs1982.me.uk',
    url='https://github.com/kevjs1982/python-eetv',
    packages=find_packages(),
    install_requires=['fuzzywuzzy', 'python-Levenshtein', 'pyteleloisirs>=3.3',
                      'requests'],
    entry_points={
        'console_scripts': ['eetv=eetv.cli:main']
    }
)
