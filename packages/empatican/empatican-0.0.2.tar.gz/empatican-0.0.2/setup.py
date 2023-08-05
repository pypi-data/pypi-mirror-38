from setuptools import setup

setup(
    name='empatican',
    version='0.0.2',
    description='Empatica Physio Utilities',
    url='http://github.com/kastman/empatican',
    author='Erik Kastman',
    author_email='erik.kastman@gmail.com',
    packages=['empatican', 'empatican.interface', 'empatican.physio'],
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
    install_requires=['requests', 'pandas'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=True)
