from distutils.core import setup
from setuptools import find_packages

setup(name='askfmcrawler',
      version='0.1.0',
      description='Python askfm crawler.',
      author='uehara1414',
      author_email='akiya.noface@gmail.com',
      url='https://github.com/uehara1414/youtube_livechat_messages',
      packages=find_packages(),
      install_requires=[
            'selenium',
      ])
