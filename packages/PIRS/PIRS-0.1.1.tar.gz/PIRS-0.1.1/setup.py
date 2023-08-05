from setuptools import setup

setup(name='PIRS',
      version='0.1.1',
      packages=['PIRS'],
      py_modules=['rank,simulations'],
      description='Prediction Interval Ranking Score',
      url='https://github.com/aleccrowell/PIRS',
      download_url='https://github.com/aleccrowell/PIRS/releases/tag/v0.1.1',
      author='Alec Crowell',
      author_email='alexander.m.crowell@gmail.com',
      license='BSD-3',
      keywords=['circadian','time series','constitutive expression','bioinformatics'],
      install_requires=['numpy','pandas','scipy','sklearn','tqdm','seaborn'],
      zip_safe=False,long_description=open('README.md').read())
