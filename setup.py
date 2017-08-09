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
    entry_points={
        'console_script': [
            'pata_password_cracker = pata_password_cracker.__main__:main'
        ],
        'pata_password_cracker.plugins': [
             'core_bio = pata_password_cracker.generators.core_bio',
             'family = pata_password_cracker.generators.family',
             'fans = pata_password_cracker.generators.fans',
             'fantasists = pata_password_cracker.generators.fantasists',
             'cryptic = pata_password_cracker.generators.cryptic',
             'free_data = pata_password_cracker.generators.free_data'
        ],
        'pata_password_cracker.encryption': [
             'md5 = pata_password_cracker.encryption.md5',
             'sha1 = pata_password_cracker.encryption.sha1',
             'sha224 = pata_password_cracker.encryption.sha224',
             'sha256 = pata_password_cracker.encryption.sha256',
             'sha384 = pata_password_cracker.encryption.sha384',
             'sha512 = pata_password_cracker.encryption.sha512',
             'bcrypt = pata_password_cracker.encryption.bcrypt'
        ],
        'pata_password_cracker.substitutors': [
             'simple = pata_password_cracker.substitutors.simple:MungSubstitutor', 
             'simplerandom = pata_password_cracker.substitutors.simplerandom:MungSubstitutorRandom' 
        ]
    }, 
    install_requires = [
        'patalib==0.0.2',
        'bcrypt'
    ]
)
