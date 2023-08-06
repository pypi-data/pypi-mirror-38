from setuptools import setup


setup(
    name='filee',
    version='0.0.1',
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'filee = filee.main:cli'
        ]
    }
)
