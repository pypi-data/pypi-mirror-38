from __future__ import absolute_import 
from setuptools import setup
from variantgrid_api import __version__

setup(name='variantgrid_api',
      version=__version__,
      description='API to connect to VariantGrid',
      url='https://github.com/SACGF/vg_api',
      author='David Lawrence',
      author_email='davmlaw@gmail.com',
      license='MIT License',
      packages=['variantgrid_api'],
      install_requires=[
          'configargparse',
          'oauthlib',
          'requests',
          'requests_oauthlib',
      ],
      scripts=['bin/vg_api',],
      zip_safe=False)
