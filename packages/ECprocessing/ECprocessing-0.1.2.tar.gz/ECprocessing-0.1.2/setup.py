from distutils.core import setup

setup(
    name='ECprocessing',
    version='0.1.2',
    author='Tim Johnson',
    author_email='tprjohnson@gmail.com',
    packages=['ecprocessing', 'ecprocessing.test'],
    url='http://pypi.python.org/pypi/ECprocessing/',
    license='LICENSE.txt',
    description='Useful preprocessing functions',
    long_description=open('README.txt').read(),
        install_requires=[
        "beautifulsoup4",
        "nltk",
    ],
)