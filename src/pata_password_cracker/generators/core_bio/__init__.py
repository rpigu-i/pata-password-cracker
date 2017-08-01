from ..gen_password import PasswordGenerator 



def process_data(k,core_bio_data,encryption_dict):
    """
    Process the core bio data
    """
    bio_passwords = PasswordGenerator(k, core_bio_data, encryption_dict).process_individual()
    return bio_passwords
