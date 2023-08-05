from setuptools import setup, find_packages

# Version managed by bumpversion, do not change it directly.
__version__ = '1.1.0'


setup(name='kongjun-client',
      description='',
      version=__version__,
      author='kongjun',
      author_email='dreamsaihua@gmail.com',
      license='Apache-2.0',
      url='https://github.com/kongjun01/eureka',
      download_url=('https://github.com/kongjun01/eureka'
                    '/archive/v' + __version__ + '.tar.gz'),
      packages=find_packages(exclude=('examples',)),
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'Topic :: Software Development',
      ],
      setup_requires=[
          'pytest-runner',
          'flake8',
      ],
      install_requires=[
          'aiohttp',
      ],
      extras_require={
          'standalone': [
              'apscheduler>=3.3.0',
          ]
      },
      tests_require=[
          'pytest-aiohttp',
          'pytest'
      ],
      entry_points={},
      zip_safe=False)
