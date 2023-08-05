from setuptools import setup

setup(name='benchlog',
      version='0.1',
      description='Logs CPU and Memory usage for project benchmarking',
      url='https://github.com/Keydex/BenchLog',
      author='Anthony Pham',
      author_email='benchlogpy@gmail.com',
      license='MIT',
      packages=['benchlog'],
      install_requires=[
          'requests',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
        )
