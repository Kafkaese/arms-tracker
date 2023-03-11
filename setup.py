from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]


setup(name='taro',
      version='0.0.1',
      author='Frederik Laubisch',
      author_email='kafkaese@gmail.com',
      install_requires=requirements,
      packages='taro')