import re
import io
from setuptools import setup, find_packages

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('empatican/__init__.py', encoding='utf_8_sig').read()).group(1)

setup(
    name='empatican',
    version=__version__,
    description='Empatica Physio Utilities',
    url='http://github.com/kastman/empatican',
    author='Erik Kastman',
    author_email='erik.kastman@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': ['empatican=empatican.cli:main'],
    },
    license='MIT',
    install_requires=['pandas', 'requests', 'tqdm'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=True)
