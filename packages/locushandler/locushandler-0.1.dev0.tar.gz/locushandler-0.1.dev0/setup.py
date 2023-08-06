from setuptools import setup

setup(
    name='locushandler',
    version='0.1dev',
    url='https://github.com/LocusAnalytics/LocusHandler',
    long_description=open('README.md').read(),
    install_requires=[
          'pandas',],
    test_suite='nose.collector',
    tests_require=['nose'],
)