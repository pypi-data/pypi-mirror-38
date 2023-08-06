from setuptools import setup, find_packages

setup(name='ijkl',
      version='0.1.0',
      description='Preprocessor for i3 Configuration',
      url='http://github.com/ankitrgadiya/ijkl',
      author='Ankit R Gadiya',
      author_email='git@argp.in',
      license='BSD 3-Clause',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['ijkl=ijkl.cli:main']
          },
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3",
          "Topic :: Utilities"
      ]
     )
