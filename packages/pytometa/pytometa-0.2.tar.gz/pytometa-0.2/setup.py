from distutils.core import setup
setup(
  name = 'pytometa',
  packages = ['pytometa'],
  version = '0.2',
  description = 'Python metadata based dict to class loader',
  author = 'Anatolii Yakushko',
  author_email = 'shaddyx@gmail.com',
  url = 'https://github.com/shaddyx/pytometa', # use the URL to the github repo
  download_url = 'https://github.com/shaddyx/pytometa/tarball/0.1',
  keywords = ['metadata', 'loader'], # arbitrary keywords
  classifiers = [],
  install_requires=[
    'typing',
  ],
)
