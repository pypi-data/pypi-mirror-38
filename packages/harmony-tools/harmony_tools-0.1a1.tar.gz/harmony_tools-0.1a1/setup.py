from setuptools import setup, find_packages

version = '0.1a1'


setup(
    name='harmony_tools',
    version=version,
    packages=find_packages(),
    package_dir={'harmony_tools': 'harmony_tools'},
    entry_points={
        'console_scripts': ['harmony_tools=harmony_tools.cli:main'],
    },
    license='MIT',
    url='https://github.com/a1fred/harmony_tools',
    author='a1fred',
    author_email='demalf@gmail.com',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite="tests",
)
