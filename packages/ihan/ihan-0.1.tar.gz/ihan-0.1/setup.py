from setuptools import setup


setup(name='ihan',
      version='0.1',
      description='IHAN Client for feeding and back filling log files',
      long_description=open('README.md').read(),
      url='https://github.com/marklit/ihan',
      author='Mark Litwintschik',
      author_email='mark@marksblogg.com',
      license='MIT',
      scripts=['bin/ihan.py',],
      install_requires=[
          "click",
          "requests",
      ],
      zip_safe=False)
