"""setup"""
import sys
import io
import os
from setuptools import setup, find_packages
from setuptools.command.test import test

here = os.path.abspath(os.path.dirname(__file__))
dataPath = os.path.join(here,"data")

"""readme"""
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

with io.open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split('\n')

"""PyTest
class PyTest(test):
    def __init__(self):
        self.test_args = []
        self.test_suite = True

    def finalize_options(self):
        test.finalize_options(self)

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)"""

name = 'exampleJupyter'
version = '1.0.0'
#path = '/usr/local/lib/python2.7/dist-packages/'+name+'-'+version+'-py2.7.egg/'
setup(
    name=name,
    version=version,
    description='ML example',
    long_description=long_description,
    url='',
    author='Jose Romero',
    author_email='josedelvalle83@gmail.com',
    license='MIT',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7'
        ],
    packages=find_packages(),
    install_requires=requirements,
    keywords='example machine learning ',
    #data_files=[('/icekit/data', ['data/icekitalgorithms.json']),
    #            ('/etc',['ice.conf']),
    #           ('/icekit',['server.sh','jobs.sh','naming.sh','README.rst']),
    #            ('/icekit/requirements',['apt-get.txt','requirements.txt','requirementsPIP.txt','downNLTK.py']),
    #            (path+'ice/prep/data/',['ice/prep/data/stopwords.csv']),
    #            (path+'ice/core/textutils/stoplists/',['ice/core/textutils/stoplists/FoxStoplists.txt']),
    #            (path+'pretrained/models/',['pretrained/models/glove.6B.50d.w2v.txt'])],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
    # test_suite='tests.ice.ds.mongo.test_ds',
    zip_safe=False,
    #entry_points={
    #        'console_scripts': [
    #            'iceInstallDependencies=installation.installDependencies:installingDependencies ',
    #            'iceStart=installation.runningServices:runningServices',
    #            'iceCreateDB = installation.creatingDB:creatingDB'
    #        ]
    #   }
)
