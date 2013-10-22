from distutils.core import setup

setup(
    name='SrmParserLite',
    version='0.0.1',
    author='verbalsaint',
    author_email='jsc9530@vmware.com',
    packages=['srmparserlite'],
    scripts=['bin/srmparser.py'],
    url='https://github.com/verbalsaintmars/srmparserlite',
    license='LICENSE',
    description='SRM Parser Lite',
    long_description=open('README.txt').read(),
    install_requires=[
        "pyyaml >= 3.0.0"
    ],
)
