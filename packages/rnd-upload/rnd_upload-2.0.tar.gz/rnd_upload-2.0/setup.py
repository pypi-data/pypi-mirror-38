from setuptools import setup

setup(name='rnd_upload',
      version='2.0',
      description='Livenviro LEQ rnd file upload',
      url='https://bitbucket.org/xorsys/rnd_upload',
      author='Mihai',
      author_email='mihai@xors.com',
      license='LICENSE',
      packages=['rnd_upload'],
      install_requires=[
          'terminaltables',
          'pytz',
          'requests'
      ],
      zip_safe=False)
