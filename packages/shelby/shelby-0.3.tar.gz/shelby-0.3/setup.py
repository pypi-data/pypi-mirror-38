from distutils.core import setup
setup(
  name = 'shelby',         # How you named your package folder (MyLib)
  packages = ['shelby'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Framework for tabular data ML competitions',   # Give a short description about your library
  author = 'Alexander Isaev',                   # Type in your name
  author_email = 'alexanderisaev23@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Taborater/shelby',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Taborater/shelby/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['ML', 'Kaggle', 'Pipeline'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'sklearn',
          'pandas',
          'scipy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Information Analysis',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)