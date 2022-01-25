
from setuptools import setup, find_packages

setup(
    name="Tracknaliser",
    version="0.1.0",
    packages=find_packages(exclude=['*.test']),
    install_requires=['matplotlib', 'pyyaml', 'numpy'],
    entry_points={
        'console_scripts': [
            'greentrack = tracknaliser_library.command:process'
        ]}    
    )
