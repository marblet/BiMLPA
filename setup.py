from setuptools import setup, find_packages
# from codecs import open
# from os import path

__author__ = ''
__license__ = "BSD-2-Clause"
__email__ = ""

# here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()


setup(name='bimlpa',
      version='0.1.2',
      license='BSD-Clause-2',
      description='Community detection in bipartite networks using multi-label propagation algorithm',
      url='https://github.com/hbkt/BiMLPA',
      author=['Hibiki Taguchi'],
      author_email='',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 5 - Production/Stable',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: BSD License',

          "Operating System :: OS Independent",

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3'
      ],
      keywords='complex-networks community-discovery labeled-graph',
      install_requires=['scikit-learn', 'matplotlib', 'networkx', ''],
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test", "BiMLPA.test", "BiMLPA.test.*"]),
      )
