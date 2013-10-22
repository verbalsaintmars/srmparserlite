from distutils.core import setup

setup(
    name='SrmParserLite',
    version='0.0.1',
    author='verbalsaint',
    author_email='jsc9530@vmware.com',
    packages=[
       'srmparserlite',
       'srmparserlite.splConfig',
       'srmparserlite.splFileManager',
       'srmparserlite.splFilter',
       'srmparserlite.splGeneral',
       'srmparserlite.splLineClass',
       'srmparserlite.splParser',
       'srmparserlite.splTraits'],
    scripts=['bin/srmparser.py'],
    data_files=[
       ('config', ['srmparserlite/config_example/splconfig.yml']),
       ('unit_test', ['srmparserlite/unit_test/unit_test.py'])],
    url='https://github.com/verbalsaintmars/srmparserlite',
    license='LICENSE',
    description='SRM Parser Lite',
    long_description=open('README.txt').read(),
    install_requires=[
        "pyyaml >= 3.0.0"
    ],
)
