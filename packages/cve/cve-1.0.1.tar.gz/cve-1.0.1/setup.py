from setuptools import setup


with open('README.md', mode='r') as f:
    long_description = f.read()

setup(
    packages=['cve'],
    name='cve',
    entry_points={'console_scripts': ['cve=cve.command:main']},
    version='1.0.1',
    description='core socialist values encoding',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chemf',
    author_email='eoyohe@gmail.com',
    url='https://github.com/feng409/core-values-encoder',
)
