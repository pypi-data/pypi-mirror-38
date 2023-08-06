from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

version_dict = {}
with open("fortdepend/_version.py") as f:
    exec(f.read(), version_dict)

name = 'fortdepend'
version = version_dict['__version__']
release = version

setup(name=name,
      version=version,
      description='Automatically generate Fortran dependencies',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Peter Hill',
      author_email='peter@fusionplasma.co.uk',
      url='https://github.com/ZedThree/fort_depend.py/',
      download_url='https://github.com/ZedThree/fort_depend.py/tarball/0.1.0',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Fortran',
      ],
      packages=['fortdepend'],
      install_requires=[
          'colorama >= 0.3.9',
          'pcpp >= 1.1.0'
      ],
      extras_require={
          'tests': ['pytest >= 3.3.0'],
          'docs': [
              'sphinx >= 1.4',
              'sphinx-argparse >= 0.2.3'
          ],
      },
      keywords=['build', 'dependencies', 'fortran'],
      entry_points={
          'console_scripts': [
              'fortdepend = fortdepend.__main__:main',
          ],
      },
      command_options={
          'build_sphinx': {
              'project': ('setup.py', name),
              'version': ('setup.py', version),
              'release': ('setup.py', release),
              'source_dir': ('setup.py', 'docs'),
          }
      },
)
