import os
from builtins import RuntimeError

from setuptools import find_packages, setup

short_description = 'A auto tester coverage report'


# noinspection PyBroadException
try:
    # noinspection PyPackageRequirements
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except RuntimeError:
    long_description = short_description

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='auto_coverage_report',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description=short_description,
    long_description=long_description,
    url='http://github.com/silviolleite/test-coverage-report',
    author='Silvio Luis',
    author_email='silviolleite@gmail.com',
    maintainer='David Guimarães',
    maintainer_email='dvdgmf@gmail.com',
    entry_points={
        'console_scripts': ['runtests=auto_coverage_report.command_line:main'],
    },
    install_requires=[
        'coverage', 'pypandoc'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit'
    ],
)
