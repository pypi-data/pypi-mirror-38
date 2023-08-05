from setuptools import setup, find_packages

# Try to convert markdown README to rst format for PyPI.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='earthport-rest-api-client',
    version='1.0.0',
    description='This API supports all services required to make cross border payments using Earthport\'s network.',
    long_description=long_description,
    author='Earthport',
    author_email='support@earthport.com',
    url='https://www.earthport.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.9.1, <3.0',
        'jsonpickle>=0.7.1, <1.0',
        'cachecontrol>=0.11.7, <1.0',
        'python-dateutil>=2.5.3, <3.0'
    ]
)