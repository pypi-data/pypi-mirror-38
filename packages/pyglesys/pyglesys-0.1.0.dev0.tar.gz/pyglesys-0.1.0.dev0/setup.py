import io
import os.path
import re

from setuptools import setup, find_packages

package = 'glesys'

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, package, '__init__.py')) as f:
    version = re.search(r'__version__ = [\'\"](.*?)[\'\"]', f.read()).group(1)

with io.open('README.rst') as f:
    readme = f.read()

requires = [
    'requests~=2.20',
    'Click~=7.0',
]

test_requires = [
    'pytest',
]

setup(
    name='pyglesys',
    version=version,
    description='Python wrapper around the GleSYS API',
    long_description=readme,
    author='Erik Jansson Agnvall',
    author_email='erikjansson90@gmail.com',
    url='https://github.com/pyglesys/pyglesys',
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    package_dir={package: package},
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=requires,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=test_requires,
    # entry_points={
    #     'console_scripts': [
    #         'glesys = glesys.cli:cli'
    #     ]
    # },
)
