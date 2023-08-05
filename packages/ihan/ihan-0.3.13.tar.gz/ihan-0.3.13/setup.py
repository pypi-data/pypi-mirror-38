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
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: System :: Networking :: Monitoring',
        ],
      zip_safe=False)
