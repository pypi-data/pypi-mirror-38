from distutils.core import setup

setup(
    name='arcadia_power_assessment',
    version='0.0',
    author='Malcolm White',
    author_email='malcolm.m14@gmail.com',
    packages=['billinfoscraper', 'billinfoscraper.test'],
    scripts=['bin/get_bill_info.py'],
    url='http://pypi.python.org/pypi/arcadia_power_assessment/',
    license='LICENSE.txt',
    description='arcadia power assessment',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4==4.6.0",
        "certif==2018.4.16",
        "chardet==3.0.4",
        "idna==2.7",
        "mock==2.0.0",
        "pb==4.2.0",
        "requests==2.19.1",
        "selenium==3.13.0",
        "six==1.11.0",
        "urllib3==1.23"
    ],
)