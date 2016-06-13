from setuptools import setup, find_packages
from chan import __release_date__

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='4chan-dl',
    version='1.0.0',
    release_data = __release_date__,
    description='4chan thread images downloader.',
    license='MIT',
    url='https://github.com/Pasithea/4chan-dl',
    packages=find_packages(),
    classifiers=[
        "License :: MIT",
        "Programming Language :: Python"
    ],
    install_requires=required,
    entry_points={
        'console_scripts': [
            '4chan-dl = chan.entry:main',
        ]
    },
)
