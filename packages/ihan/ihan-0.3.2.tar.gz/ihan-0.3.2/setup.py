from setuptools import setup


setup(name='ihan',
      version='0.3.2',
      description='IHAN Client for feeding and back filling log files',
      url='https://github.com/marklit/ihan',
      author='Mark Litwintschik',
      author_email='mark@marksblogg.com',
      license='MIT',
      scripts=['bin/ihan',],
      install_requires=[
          "Click",
          "requests",
      ],
      zip_safe=False)
