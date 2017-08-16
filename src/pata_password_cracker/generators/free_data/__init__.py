from ..gen_password import PasswordGenerator


class FreeDataGenerator():

    def process_data(
            self,
            k,
            words,
            free_bio_data,
            encryption_dict,
            substitutors_dict):
        """
        Process the free bio data
        """
        free_bio_passwords = PasswordGenerator(
            k,
            words,
            free_bio_data,
            encryption_dict,
            substitutors_dict).process_individual()
        return free_bio_passwords
