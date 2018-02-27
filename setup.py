from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='gitsherlock',
        version='0.4',
        description='A GitHub mining tool for research purposes.',
        long_description=long_description,
        url='https://github.com/omazhary/git-sherlock',
        author='omazhary',
        author_email='omazhary@gmail.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Information Analysis',
        ],
        keywords='data collection scrape research',
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        install_requires=[
            'argparse',
            'bs4',
            'requests',
        ],
        extras_require={},
        package_data={},
        data_files=[],
        scripts=[],
        entry_points={
            'console_scripts': [
                'gitsherlock=gitsherlock:main',
            ],
        },
        zip_safe=False
)
