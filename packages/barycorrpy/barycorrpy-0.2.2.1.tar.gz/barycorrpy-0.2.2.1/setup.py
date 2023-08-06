from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()



setup(name='barycorrpy',
      version='0.2.2.1',
      description='Barycentric Velocity correction at 1 cm/s level',
      long_description=readme(),
      url='https://github.com/shbhuk/barycorrpy',
      author='Shubham Kanodia',
      author_email='shbhuk@gmail.com',
      install_requires=['astropy>2','jplephem','numpy','scipy','astroquery'],
      packages=['barycorrpy'],
      license='GPLv3',
      classifiers=['Topic :: Scientific/Engineering :: Astronomy'],
      keywords='Barycentric Correction Astronomy Spectroscopy Radial Velocity',
      include_package_data=True
      )
      
