from ..gen_password import PasswordGenerator


class FreeDataGenerator():
    """
    Any data that does not fit into 
    a specific category with advanced
    processing is considered free data.
    This class handles the processing
    of free data.
    """ 
    def process_data(
            self,
            k,
            words,
            free_bio_data,
            encryption_dict,
            substitutors_dict):
        """
        Process the free bio data.
        At the moment we simply pass
        off to the password generator.
        """
        free_bio_passwords = PasswordGenerator(
            k,
            words,
            free_bio_data,
            encryption_dict,
            substitutors_dict).process_individual()
        return free_bio_passwords
