from setuptools import setup

setup(name='friendlyscore',
      version='0.3',
      description='FriendlyScore API client for Cloud and WhiteLabel solution',
      url='https://github.com/FriendlyScore/FriendlyScore-Python-SDK',
      author='Rafał Toboła',
      author_email='r.tobola@friendlyscore.com',
      license='MIT',
      packages=['friendlyscore'],
      install_requires=[
          'requests'
      ],
      zip_safe=False)
