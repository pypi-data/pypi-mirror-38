from setuptools import setup

setup(name='RequestIdLogger',
      version='0.1',
      description='Logger with request id',
      url='',
      author='Atman Corp',
      author_email='corp@atman.com',
      license='MIT',
      packages=['request_id_logger'],
      install_requires=[
          'flask-log-request-id',
          'Flask'
      ],
      zip_safe=False)
