from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='benchlog',
      version='0.3.dev3',
      description='Log CPU, GPU and Memory usage for a project overtime and send to server',
      url='https://github.com/Keydex/BenchLog',
      author='Anthony Pham',
      author_email='benchlogpy@gmail.com',
      license='MIT',
      packages=['benchlog'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=[
          'requests',
          'psutil',
          'GPUtil'
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
        )
