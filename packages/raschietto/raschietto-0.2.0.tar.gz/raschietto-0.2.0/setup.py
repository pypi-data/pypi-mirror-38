from setuptools import setup

setup(
    name='raschietto',
    packages=['raschietto'],
    version='0.2.0',
    description='A simple web scraping library',
    author='Matteo Ronchetti',
    author_email='matteo@ronchetti.xyz',
    url='https://gitlab.com/matteo-ronchetti/raschietto',
    install_requires=['lxml==4.2.5', 'cssselect==1.0.3', 'requests==2.20.1', 'urllib3==1.24.1'],
    keywords=['scraping', 'web'],  # arbitrary keywords
    classifiers=['Programming Language :: Python :: 3'],
)
