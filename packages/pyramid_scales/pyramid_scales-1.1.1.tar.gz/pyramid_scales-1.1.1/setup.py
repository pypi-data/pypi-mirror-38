"""Viewing scales metrics from Pyramid"""
from setuptools import setup, find_packages
import glob


setup(
    name='pyramid_scales',
    version='1.1.1',

    install_requires=[
        'scales',
        'setuptools',
    ],

    extras_require={
        'test': [
            'pyramid',
            'pytest',
            'webtest',
        ],
    },

    author='Wolfgang Schnerring <wosc@wosc.de>',
    author_email='wosc@wosc.de',
    license='BSD',
    url='https://github.com/wosc/pyramid_scales',

    keywords='',
    description=__doc__.strip(),
    long_description='\n\n'.join(open(name).read() for name in (
        'README.txt',
        'HACKING.txt',
        'CHANGES.txt',
    )),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('', glob.glob('*.txt'))],
    zip_safe=False,
)
