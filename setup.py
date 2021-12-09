from distutils.core import setup
setup(
  name = 'teepy',
  packages = ['teepy'],
  version = '0.3.1',
  license = 'MIT',
  description = 'Tech Engineering Exam in Python',
  author = 'William Long',
  author_email = 'admin@longapalooza.com',
  url = 'https://github.com/longapalooza/teepy',
  keywords = ['Tech', 'Exam', 'Engineering'],
  install_requires = [
          'beautifulsoup4',
          'cefpython3',
          'pint',
          'pyppeteer',
          'xlsxwriter',
      ],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  package_data = {'': ['*']},
)