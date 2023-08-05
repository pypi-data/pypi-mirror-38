from setuptools import setup

setup(name='rnd_upload',
      version='1.0',
      description='Livenviro LEQ rnd file upload',
      url='https://bitbucket.org/xorsys/rnd_upload',
      author='Mihai',
      author_email='mihai@xors.com',
      license='',
      packages=['rnd_upload'],
      install_requires=[
          'terminaltables',
          'sqlalchemy',
          'pytz',
          'mysqlclient',
          'requests'
      ],
      zip_safe=False)
