from setuptools import setup, find_packages
from setuptools.command.install import install
import io

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
        print "Installing WordNet"
        install.run(self)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')

setup(
    name='pata-password-cracker',
    version='1.1.0',
    description='Pataphysical passwork cracker using personal data',
    long_description=long_description,
    maintainer='patamechanix',
    license='MIT',
    url='https://github.com/patamechanix/pata-password-cracker',
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
        'patalib==1.0.1',
        'bcrypt'
    ],
    cmdclass={
        'install': InstallNLTKDependencies
    }
)
