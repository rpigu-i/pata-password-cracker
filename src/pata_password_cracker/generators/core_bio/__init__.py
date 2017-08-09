from ..gen_password import PasswordGenerator 


class CoreBioGenerator():
    """
    Generator for core biographic
    data
    """ 

    def process_data(self,k,core_bio_data,encryption_dict,substitutors_dict):
        """
        Process the core bio data
        """
        bio_passwords = PasswordGenerator(k, core_bio_data, encryption_dict, substitutors_dict).process_individual()
        return bio_passwords
