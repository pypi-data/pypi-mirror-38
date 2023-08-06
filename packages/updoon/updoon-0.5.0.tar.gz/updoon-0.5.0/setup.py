from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='updoon',
      version='0.5.0',
      description='classes and functions to download or scrape data',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/waalfisk/updoon',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['updoon'],
      install_requires=[
          'numpy', 'urllib3', 'setuptools', 'datetime',
          'nose', 'bs4', 'pandas'],
      python_requires='>=3',
      zip_safe=False)
