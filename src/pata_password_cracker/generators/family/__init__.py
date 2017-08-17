from ..gen_password import PasswordGenerator
from ..date_name_mixin import DateNameMixin

class FamilyGenerator(DateNameMixin):
    """
    Class for generating 
    family based data.
    """
    family_data = {}
    cat = ""
    encryption_dict = {}
    substitutors_dict = {}
    words = []

    def process_data(
            self,
            k,
            words,
            family_bio_data,
            encryption_dict,
            substitutors_dict):
        """
        Process the family bio data
        """
        self.family_data = family_bio_data
        self.cat = k
        self.words = words
        self.encryption_dict = encryption_dict
        self.substitutors_dict = substitutors_dict

        family_passwords = self.process_individual()
        return family_passwords

    def process_individual(self):
        """
        Process an individuals data
        to generate a list of potential
        passwords.
        """
        individual = {}
        pata_passwords = []

        for ind in self.family_data:
            for bio, values in ind.iteritems():
                pata_passwords.append(self.name_dob(values))
                pata_passwords.append(
                    PasswordGenerator(
                        self.cat,
                        self.words,
                        values,
                        self.encryption_dict,
                        self.substitutors_dict).process_individual())
                individual[bio] = pata_passwords

            pata_passwords = []

        return individual

