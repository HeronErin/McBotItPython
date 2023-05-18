from setuptools import setup
from mcbotit import VERSION

with open("README.md", "r", encoding='utf-8') as file:
  long_description = file.read()


setup(
  name             = 'McBotIt',
  version          = VERSION,
  description      = 'A python library for fully controlling the player in Minecraft',
  author           = 'HeronErin',
  url              = 'https://github.com/HeronErin/McBotItPython',
  license          = "GPLv3",
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages         = ['mcbotit'],
  classifiers      = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
  ]
)
