import os,sys
from setuptools import setup
from setuptools.command.install_scripts import install_scripts
from distutils.command.build_scripts import build_scripts
from subprocess import call
from os.path import dirname
from shutil import copy2

class mpplBuild(build_scripts):
    def run(self):
        call('./init.sh')
        call('make')
        build_scripts.run(self)
class mpplInstall(install_scripts):
    def run(self):
        bdir = dirname(sys.executable)
        try:
           copy2('mppl',bdir)
           copy2('mppl.sys',bdir)
           copy2('mppl.std',bdir)
           copy2('mppl.BASIS',bdir)
           install_scripts.run(self)
        except:
           bdir = '/usr/local/bin'
           copy2('mppl',bdir)
           copy2('mppl.sys',bdir)
           copy2('mppl.std',bdir)
           copy2('mppl.BASIS',bdir)
           install_scripts.run(self)


setup(name='mppl',
      version='1.0',
      description='More Productive Programming Language',
      maintainer='LLNL',
      maintainer_email='meyer8@llnl.gov',
      url='https://w3.pppl.gov/ntcc/MPPL',
      scripts=['mppl'],
      cmdclass={
          'build_scripts':mpplBuild,
          'install_scripts':mpplInstall

      }
     )

