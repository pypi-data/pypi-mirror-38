import codecs
import os
from setuptools import setup


this_directory = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_directory, 'README.md'), 'r', encoding='utf8') as f:
    long_description = f.read()
requirements = []
with codecs.open(os.path.join(this_directory, 'requirements.txt'), 'r', encoding='utf8') as f:
    for line in f:
        requirements.append(line)

setup(name='textnormaliser',
      version='1.0.0',
      description='A python package that runs a series of operations over text to decorate a corpus',
      url='https://github.com/dust10141/text-normaliser',
      author='Will Sackfield',
      author_email='will.sackfield@gmail.com',
      license='MIT',
      packages=['textnormaliser'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=requirements,
      entry_points={
        'console_scripts': [
            'textnormaliser = textnormaliser:_main'
        ]
      })
