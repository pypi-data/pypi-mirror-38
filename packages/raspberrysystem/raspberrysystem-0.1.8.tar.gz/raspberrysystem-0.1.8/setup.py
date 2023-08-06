import setuptools

def readme():
  '''Get long description from readme file'''
  with open('README.md') as f:
    return f.read()


def version():
  '''Get version from version file'''
  with open('VERSION') as f:
    return f.read().strip()

setuptools.setup(name='raspberrysystem',
      version=version(),
      description='The funniest joke in the world',
      long_description=readme(),
      url='http://github.com/raubreywhite/raspberrysystem',
      author='Richard',
      author_email='w@rwhite.no',
      license='MIT',
      packages=['raspberrysystem'],
      zip_safe=False)
