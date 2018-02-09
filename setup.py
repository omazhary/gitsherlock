from setuptools import setup

setup(
        name='gitsherlock',
        version='0.1',
        description='A GitHub mining tool for research purposes.',
        url='https://github.com/omazhary/git-sherlock',
        author='omazhary',
        author_email='omazhary@gmail.com',
        license='MIT',
        packages=['gitsherlock'],
        install_requires=[
            'argparse',
            'bs4',
        ],
        scripts=['bin/gitsherlock'],
        zip_safe=False
)
