from setuptools import setup, find_packages
from os import path
import configparser

config = configparser.ConfigParser()
config.read('S3MPython.conf')
VERSION = config['SYSTEM']['version']
RMVERSION = config['SYSTEM']['rmversion']
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='S3MPython',
    version=VERSION,
    description='Python implementation of the S3Model https://datainsights.tech/S3Model/ specifications version: ' + RMVERSION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Timothy W. Cook',
    author_email='tim@datainsights.tech',
    url='https://datainsights.tech/',
    download_url='https://github.com/DataInsightsInc/S3MPython/archive/' + VERSION + '.tar.gz',
    keywords=['context rdf xml machine learning data-centric semantic interoperability semantics agi'],
    tests_require=['pytest', ],
    setup_requires=['pytest-runner', ],
    python_requires='>=3.7',
    packages=['S3MPython'],
    package_dir={'S3MPython': 'S3MPython'},
    package_data={'docs': ['docs/*']},
    data_files=[('s3model', ['s3model/s3model_3_1_0.xsl', 's3model/s3model_3_1_0.xsd', 's3model/s3model_3_1_0.rdf',
                             's3model/s3model.owl', 's3model/dm-description.xsl']), ('', ['S3MPython.conf', 'acs.txt'])],
    install_requires=[
        'requests>=2.20',
        'lxml>=4.2',
        'xmltodict>=0.11',
        'cuid>=0.3',
        'validator-collection>=1.2',
        'pytz>=2018',
        'exrex>=0.10'
      ],
    classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Customer Service',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Financial and Insurance Industry',
                   'Intended Audience :: Healthcare Industry',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Legal Industry',
                   'Intended Audience :: Manufacturing',
                   'Intended Audience :: Other Audience',
                   'Intended Audience :: Religion',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                 ],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/DataInsightsInc/S3MPython/issues',
        'Training': 'https://DataInsights.tech/training',
        'Source': 'https://github.com/DataInsightsInc/S3MPython/',
    },
)
