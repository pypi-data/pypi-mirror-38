#!/usr/bin/env python

from distutils.core import setup

setup(name='datamaestro',
    version='0.1',
    description='Dataset management',
    author='Benjamin Piwowarski',
    author_email='benjamin@bpiwowar.net',
    url='https://github.com/bpiwowar/datasets',
    packages=['datamaestro'],
    package_dir={'datamaestro': 'datamaestro'},
    install_requires = [ 'Click' ],
    package_data={'datamaestro': ['LICENSE', 'datamaestro/repositories.yaml']},
    data_files = [
        
    ],
    entry_points = {
        'console_scripts': [
            'datasets = datasets.__main__:main',                  
        ],         
        'mkdocs.plugins': [
                'datasets = datasets.commands.site:DatasetGenerator',
        ]
    },
)
