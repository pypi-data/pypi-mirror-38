from setuptools import setup, find_packages

setup(
    name = 'XYLLibrary',
    version = '0.3.0',
    keywords = ('XYLLibrary', 'robot'),
    description = 'python 3.X',
    license = 'MIT License',

    author = 'zy',
    author_email = '84497503@qq.com',

    packages = find_packages(),
    install_requires=['requests>=2.9.1','jsonschema>=2.5.1','robotframework-selenium2library>=1.7.4'],
    platforms = 'any',
)