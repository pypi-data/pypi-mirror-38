#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

try:
    from setuptools import setup

except:
    from distutils.core import setup
    pass

from gtkmvc3 import get_version


setup(name="python-gtkmvc3-dlr",
      version=".".join(map(str, get_version())), 
      description="Model-View-Controller and Observer patterns for developing pygtk-based applications",
      author="Roberto Cavada, Sebastian Brunner, Rico Belder, Franz Steinmetz",
      author_email="roboogle@gmail.com",
      maintainer='Sebastian Brunner',
      maintainer_email='sebastian.brunner@dlr.de',
      license="LGPL",
      url="https://github.com/roboogle/gtkmvc3/",
      keywords=('mvc', ),

      packages=['gtkmvc3', 'gtkmvc3.support', 'gtkmvc3.adapters', 'gtkmvc3.progen'],
      package_data={'gtkmvc3.progen': ['progen.ui']},
      scripts=['scripts/gtkmvc3-progen'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          ],
      
     )
