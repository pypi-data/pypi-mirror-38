from distutils.core import setup

setup(
  name = 'radfil',
  packages = ['radfil'],
  version = '1.1.1',
  description = 'Build radial density profiles for interstellar filaments. See Zucker & Chen 2018 for full details. Contact catherine.zucker@cfa.harvard.edu & hopechen@utexas.edu with questions/comments!',
  author = ['Catherine Zucker', 'Hope Chen'],
  author_email = 'catherine.zucker@cfa.harvard.edu',
  url = 'http://github.com/catherinezucker/RadFil', # use the URL to the github repo
  download_url = 'https://api.github.com/repos/catherinezucker/radfil/zipball/master',
  keywords = ['astrophysics', 'radfil', 'filaments'], # arbitrary keywords
  classifiers = [],
  install_requires=[
      'numpy',
      'scipy',
      'matplotlib',
      'astropy',
      'shapely',
      'sklearn',
      'scikit-image',
      'networkx',
      'pandas'
  ]
)
