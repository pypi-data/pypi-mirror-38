from setuptools import setup,find_packages

setup(
  name = 'datachimp',
  packages = find_packages(),
  version = '0.0.1',
  description = 'Python client to version your data ',
  entry_points='''
        [console_scripts]
        datachimp=datachimp.cli:cli
    ''',
  author = 'Samir Madhavan',
  author_email = 'samir.madhavan@gmail.com',
  url = 'https://www.modelchimp.com',
  keywords = ['modelchimp', 'ai', 'datascience', 'data', 'versioning'],
  install_requires=[
          'requests',
          'future',
          'six',
          'websocket-client',
          'pytz',
          'cloudpickle',
          'click',
      ],
  classifiers = [],
)
