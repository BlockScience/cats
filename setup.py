from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(name="pycats",
      version="0.0.0",
      description="CATs",
      author='Joshua E. Jodesty',
      author_email='joshua@block.science',
      license='LICENSE.txt',
      packages=find_packages(),
      install_requires=install_requires,
      python_requires='>=3.9.7'
)