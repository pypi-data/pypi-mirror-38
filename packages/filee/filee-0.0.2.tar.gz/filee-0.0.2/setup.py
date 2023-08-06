from setuptools import find_packages, setup


setup(
    name='filee',
    version='0.0.2',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'filee = filee.main:cli'
        ]
    }
)
