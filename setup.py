from setuptools import setup, find_packages


setup(
    name='pata-password-cracker',
    version='0.0.1',
    description='Intelligence passwork cracker using personal data',
    maintainer='Andy Dennis',
    license='MIT',
    url='https://github.com/andydennis/pata-password-cracker',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    install_requires = [
        'patalib==0.0.2',

    ]
)
