import os
from setuptools import setup, find_packages

version = '0.1'

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as fp:
    longdesc = fp.read()

# with open(os.path.join(here, 'CHANGELOG.rst')) as fp:
#     longdesc += "\n\n" + fp.read()


setup(
    name='ghx',
    version=version,
    packages=find_packages(),
    url='https://github.com/rshk/ghx',
    license='BSD License',
    author='Samuele Santi',
    author_email='sam@reinventsoftware.io',
    description='Run scripts from Github on the fly',
    long_description=longdesc,
    install_requires=['click'],
    # tests_require=tests_require,
    # test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.0',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',

        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: Stackless',
    ],
    entry_points={
        'console_scripts': ['ghx=ghx.cli:main'],
    },
    package_data={'': ['README.rst', 'CHANGELOG.rst']},
    include_package_data=True,
    zip_safe=False)
