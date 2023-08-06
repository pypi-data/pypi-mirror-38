from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='poeditor_api_wrapper',
      version='0.1',
      description='Python Wrapper for POEditor V2 API',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='poeditor api v2',
      url='http://bitbucket.org/asmuth444/poeditor_api_wrapper',
      author='Abhishek Roul',
      author_email='asmuth444@gmail.com',
      license='MIT',
      packages=['poeditor_api_wrapper'],
      install_requires=[
          'requests',
          'urllib3'
      ],
      include_package_data=True,
      zip_safe=False)