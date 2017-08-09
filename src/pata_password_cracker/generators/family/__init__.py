from family_generator import FamilyPasswordGenerator

def process_data(k, family_bio_data, encryption_dict, substitutors_dict):
    """
    Process the family bio data
    """
    family_passwords = FamilyPasswordGenerator(k, family_bio_data, encryption_dict, substitutors_dict).process_individual()
    return family_passwords
