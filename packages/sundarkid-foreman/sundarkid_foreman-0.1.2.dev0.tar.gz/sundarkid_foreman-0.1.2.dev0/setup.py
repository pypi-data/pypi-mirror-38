from setuptools import setup

setup(
    name='sundarkid_foreman',
    version='0.1.2dev',
    packages=['foreman', ],
    author='sundarkid',
    author_email='sundareswaran25@gmail.com',
    license='MIT',
    long_description=open('README.mkd').read(),
    install_requires=[
        'requests',
    ],
)
