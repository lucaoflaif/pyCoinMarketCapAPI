from setuptools import setup

setup(name='pyCoinMarketCapAPI',
      version='0.2',
      description="Python support for coimarketcap's APIs with cache and timezones support.",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',

      ],
      keywords="cryptocurrency bitcoin api market",
      url='https://github.com/lucaoflaif/pyCoinMarketCapAPI',
      author='Luca Di Vita',
      author_email='d.v.luca99@gmail.com',
      license='MIT',
      packages=['coinmarketcapapi'],
      install_requires=[
          'requests',
          'pytz',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)
