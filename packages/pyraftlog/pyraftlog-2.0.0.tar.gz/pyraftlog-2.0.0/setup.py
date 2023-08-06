from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pyraftlog',
      version='2.0.0',
      description='Pure Python implementation of the RAFT concencous algorithm',
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Operating System :: OS Independent',
      ],
      author='Peter Scopes',
      author_email='peter.scopes@nccgroup.trust',
      license='Copyright 2018 NCC',
      packages=['pyraftlog'],
      install_requires=[
          'msgpack>=0.5.6',
          'redis>=2.10.6',
      ],
      entry_points={
          'console_scripts': ['pyraftlog-mock=pyraftlog.mock:main']
      },
      include_package_data=True,
      zip_safe=False)
