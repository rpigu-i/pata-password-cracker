from ..gen_password import PasswordGenerator
from ..date_name_mixin import DateNameMixin


class CoreBioGenerator(DateNameMixin):
    """
    Generator for core biographic
    data
    """
    cat = ""
    encryption_dict = {}
    substitutors_dict = {}
    words = []

    def process_data(
            self,
            k,
            words,
            core_bio_data,
            encryption_dict,
            substitutors_dict):
        """
        Process the core bio data
        """
        self.cat = k
        self.words = words
        self.encryption_dict = encryption_dict
        self.substitutors_dict = substitutors_dict

        bio_passwords = []
        bio_passwords.append(self.name_dob(core_bio_data))
        bio_passwords.append(PasswordGenerator(
            k,
            words,
            core_bio_data,
            encryption_dict,
            substitutors_dict).process_individual())
        return bio_passwords
