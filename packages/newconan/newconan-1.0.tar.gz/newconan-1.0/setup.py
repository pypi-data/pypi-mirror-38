from setuptools import setup

setup(name='newconan',
      version='1.0',
      description='New cmake project based on conan',
      url='https://github.com/wumo/newconan',
      author='wumo',
      license='MIT',
      packages=['newconan'],
      install_requires=[
        'conan',
      ],
      zip_safe=False)
