from setuptools import setup

setup(name='simplemachinelearning',
      version='0.0.1',
      description='Package to simplify machine learning',
      url='https://github.com/nickolastheodoulou/simplemachinelearning.git',
      author='nickolastheodoulou & DenJev',
      author_email='nickolastheodoulou@hotmail.com',
      license='MIT',
      packages=['simplemachinelearning'],
      install_requires=['pandas', 'sklearn', 'scipy', 'seaborn', 'numpy'],
      zip_safe=False)

