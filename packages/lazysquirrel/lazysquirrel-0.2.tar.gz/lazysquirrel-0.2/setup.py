from setuptools import setup

setup(name='lazysquirrel',
      version='0.2',
      description='Initialize your programs & servers in one click',
      url='https://github.com/omarking05/linux-init-script',
      author='Omar Ahmed',
      author_email='omar.ahmed.oaaem@gmail.com',
      license='MIT',
      packages=['lazysquirrel'],
      zip_safe=False,
      entry_points = {
        'console_scripts': ['lazysquirrel=lazysquirrel.command_line:main'],
      })