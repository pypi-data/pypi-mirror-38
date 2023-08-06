from distutils.core import setup
setup(
  name = 'supercog',
  packages = ['supercog'],
  version = '1.10.1',
  license='MIT',
  description = 'A project that assists in making a Discord bot. Includes HTML and Markdown support.',
  author = 'FellowHashbrown',
  author_email = 'fellowhashbrown@gmail.com',
  url = 'https://github.com/FellowHashbrown/supercog',
  download_url = 'https://github.com/FellowHashbrown/supercog/archive/v1.10.1.tar.gz',
  keywords = ["discord", "bot", "cogs", "extensions", "command", "category", "html", "markdown"],
  install_requires=[

  ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)