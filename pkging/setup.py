from setuptools import setup, find_packages

short_description = "CATs"

long_description = "CATs"

name = "CATs"
version = "0.0.0"

setup(name=name,
      version=version,
      description=short_description,
      long_description=long_description,
      # url=...,
      author='Joshua E. Jodesty',
      author_email='joshua@block.science',
      # license='LICENSE.txt',
      packages=find_packages(),
      install_requires=[
            "pandas",
            "funcy",
            "dill",
            "pathos",
            "numpy",
            "pytz"
             ],
      python_requires='>=3.12.0'
)