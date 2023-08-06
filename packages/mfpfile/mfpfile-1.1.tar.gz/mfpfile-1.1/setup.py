"""
USAGE: 
   o install in develop mode: navigate to the folder containing this file,
                              and type 'python setup.py develop --user'.
                              (ommit '--user' if you want to install for 
                               all users)                           
"""
from setuptools import setup

setup(name='mfpfile',
      version='1.01',
      description='Package to handle reading of ibw files created with MFP devices.',
      url='',
      author='Ilyas Kuhlemann',
      author_email='ilyasp.ku@gmail.com',
      license='MIT',      
      entry_points={
          "console_scripts": [],
          "gui_scripts": []
      },
      install_requires=['numpy',
                        'igor'],
      packages=['mfpfile'],
      zip_safe=False)
