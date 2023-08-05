from setuptools import setup, find_packages

setup(
    name="koa_like_flask_logger",
    version="0.0.2",
    description="Add a koa-like logger for flask",
    url='https://github.com/paradoxxxzero/koa_like_flask_logger',
    author='Florian Mounier',
    packages=find_packages(),
    install_requires=['flask'],
    license='MIT',
)
