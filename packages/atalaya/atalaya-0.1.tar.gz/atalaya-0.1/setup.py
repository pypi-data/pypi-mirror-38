from setuptools import setup, find_packages

setup(name='atalaya',
      version='0.1',
      python_requires='>=3.6',
      description='Atalaya is a logger for pytorch.',
      url='https://bitbucket.org/dmmlgeneva/frameworks/src/master/atalaya/',
      author='jacr',
      author_email='joao.candido@hesge.ch',
      license='MIT',
      packages=find_packages(),
      install_requires=[
                        'torch',
                        'visdom>=0.1.8.5',
                        'tensorboardX>=1.4'
      ],
      zip_safe=False)