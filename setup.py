from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'space-time-astar',         # How you named your package folder (MyLib)
  packages = ['stastar'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A* search algorithm with an added time dimension to deal with dynamic obstacles.',   # Give a short description about your library
  author = 'Haoran Peng',                   # Type in your name
  author_email = 'gavinsweden@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/GavinPHR/Space-Time-AStar',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/GavinPHR/Space-Time-AStar/archive/v0.1-alpha.tar.gz',    # I explain this later on
  keywords = ['astar-algorithm', 'obstacle-avoidance', 'time-dimension'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  long_description=long_description,
  long_description_content_type='text/markdown'
)

# Tutorial at https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56