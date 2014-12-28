from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = requirements_file.readlines()

setup(
    name='tgallery',
    version='0.1',
    description='backend for tgallery',
    long_description='''A tornado gallery server.''',
    author='Martin Hoefling',
    author_email='martin.hoefling@gmx.de',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
    url='none',
    packages=find_packages(exclude=["*_tests"]),
    package_data={
        'tgallery': ['static/*'],
    },
    test_suite='nose.collector',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['tgallery = tgallery.services.app:main'],
        }
)
