from distutils.core import setup
setup(
  name = 'beamInfluxDBWriter',         # How you named your package folder (MyLib)
  packages = ['beamInfluxDBWriter'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A connector where you can write from apache beam pipeline to influxdb',   # Give a short description about your library
  author = 'Hussein Khaled',                   # Type in your name
  author_email = 'husseinkk96@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ThinkBigEg/beam_influxDB_connector',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ThinkBigEg/beam_influxDB_connector/archive/0.3.tar.gz',    # I explain this later on
  keywords = ['iot', 'influxdb', 'beam'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'influxdb',
          'apache_beam[gcp]',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)