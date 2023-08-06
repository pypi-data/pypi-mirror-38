from setuptools import setup, find_packages

setup(
    name='shortesttrack-sdk',
    version='1.3.1',
    description='SDK for work with ShortestTrack API',
    packages=find_packages(),
    install_requires=[
        'URLObject',
        'requests',
        'setuptools',
        'shortesttrack-tools==0.1.9'
    ],
    author='Shortest Track',
    author_email='mpyzhov@shtr.io',
    license='MIT'
)
