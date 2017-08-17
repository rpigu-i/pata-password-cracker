from setuptools import setup, find_packages
from setuptools.command.install import install


class InstallNLTKDependencies(install):
    """
    Install any dependencies needed by
    the library from the NLTK installer
    for example corpora.
    """

    def run(self):
        """
        Add NLTK installation commands
        here
        """
        from nltk import wordnet
        print "Hello"
        install.run(self)


setup(
    name='pata-password-cracker',
    version='1.0.1',
    description='Pataphysical passwork cracker using personal data',
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
            'core_bio = pata_password_cracker.generators.core_bio:CoreBioGenerator',
            'family = pata_password_cracker.generators.family:FamilyGenerator',
            'free_data = pata_password_cracker.generators.free_data:FreeDataGenerator'
        ],
        'pata_password_cracker.encryption': [
            'md5 = pata_password_cracker.encryption.md5:MD5Encryption',
            'sha1 = pata_password_cracker.encryption.sha1:SHA1Encryption',
            'sha224 = pata_password_cracker.encryption.sha224:SHA224Encryption',
            'sha256 = pata_password_cracker.encryption.sha256:SHA256Encryption',
            'sha384 = pata_password_cracker.encryption.sha384:SHA384Encryption',
            'sha512 = pata_password_cracker.encryption.sha512:SHA512Encryption',
            'bcrypt = pata_password_cracker.encryption.bcrypt:BcryptEncryption'
        ],
        'pata_password_cracker.substitutors': [
            'simple = pata_password_cracker.substitutors.simple:MungSubstitutor',
            'simplerandom = pata_password_cracker.substitutors.simplerandom:MungSubstitutorRandom',
            'common = pata_password_cracker.substitutors.common:MungSubstitutorCommon'
        ]
    },
    install_requires=[
        'patalib==1.0.0',
        'bcrypt'
    ],
    cmdclass={
        'install': InstallNLTKDependencies
    }
)
