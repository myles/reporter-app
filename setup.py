import os

from setuptools import setup

from reporter_app import __version__, __project_name__, __project_link__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = __project_name__,
    version = __version__,
    
    description = "A Python Library for the iOS application Reporter.",
    
    author = "Myles Braithwaite",
    author_email = "me@mylesbraithwaite.com",
    
    license = 'BSD',
    
    keywords = 'reporter',
    
    url = __project_link__,
    
    long_description = read('README.rst'),
    
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    
    install_requires = [
        'pytz',
        'tzlocal'
    ],
    
    extra_require = {
        'cli': [ 'clint', ]
    },
    
    entry_points = {
        'console_scripts': [
            'py-reporter = reporter.cli:main [cli]'
        ]
    }
)