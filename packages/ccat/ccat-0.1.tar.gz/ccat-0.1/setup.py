from setuptools import setup, find_packages

setup(
    name='ccat',
    version='0.1',
    description='modules for bit.io trading platform',
    url='https://github.com/bliiir/bit',
    author='bliiir',
    author_email='hello@bit.io',
    license='MIT',
    packages=find_packages(),
    install_requires=[
          'ccxt',
          'pandas',
          'numpy',
          'psycopg2',
          'SQLAlchemy'
      ],
    zip_safe=False
    )
