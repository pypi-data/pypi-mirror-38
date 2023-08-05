import os
from   setuptools import setup


dir_path = os.path.dirname(os.path.realpath(__file__))

_read = lambda filename: open(os.path.join(dir_path, filename)).read()

setup(name='ihan',
      version=_read('VERSION'),
      description='IHAN Client for feeding and back filling log files',
      long_description=_read('docs/index.rst'),
      long_description_content_type='text/x-rst',
      url='https://www.ihan.ee/',
      project_urls={
        "Bug Tracker": "https://github.com/marklit/ihan/issues",
        "Documentation": "https://ihan.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/marklit/ihan",
      },
      author='Mark Litwintschik',
      author_email='mark@marksblogg.com',
      license='MIT',
      packages=['ihan'],
      scripts=['bin/ihan',],
      install_requires=[
          "Click",
          "requests",
      ],
      zip_safe=False)
