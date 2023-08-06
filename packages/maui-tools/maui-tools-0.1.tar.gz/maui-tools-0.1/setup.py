from setuptools import setup

setup(name='maui-tools',
      version='0.1',
      description="Multi-omics Autoencoder Integration",
      author='Jonathan Ronen',
      license='GPLv3',
      author_email='yablee@gmail.com',
      url='https://github.com/BIMSBbioinfo/maui',
      packages=['maui'],
      install_requires=[
          'pytest',
          'numpy',
          'pandas',
          'scipy',
          'scikit-learn',
          'keras',
          'tensorflow'
      ],
)
