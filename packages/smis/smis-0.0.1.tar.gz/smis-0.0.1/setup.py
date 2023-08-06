from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='smis',
    version='0.0.1',
    description='Serverless microservices is smis',
    url='https://github.com/zhammer/smis',
    packages=('smis',),
    author='Zach Hammer',
    author_email='zach.the.hammer@gmail.com',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
