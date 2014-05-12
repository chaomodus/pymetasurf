from setuptools import setup

setup(name='pymetasurf',
      version='0.1.0',
      description='A ctypes-based binding for metasurface',
      url='https://gitorious.org/pymetasurf/pymetasurf/',
      author='Cas Rusnov',
      author_email='rusnovn@gmail.com',
      license='LGPL',
      packages=['pymetasurf'],
      install_requires=[
          'ctypes',
      ],
      zip_safe=False)
