from gen_password import PasswordGenerator

class DateNameMixin(object):
    """
    Mixin for supporting date and
    name processing.
    """ 
    def name_dob(self, values):
        """
        Generate name/dob passwords.
        This relies on specific values provided in
        the input YAML file for each individual. 
        Namely:

        first_name
        last_name
        dob      

        """
        name_dob_combo = {}

        if values['first_name'] and values['dob']:
            name_dob_combo['first_name_dob'] = self.date_and_name_processor(
                values['first_name'], values['dob'])

        if values['last_name'] and values['dob']:
            name_dob_combo['last_name_dob'] = self.date_and_name_processor(
                values['last_name'], values['dob'])

        name_dob_combo = PasswordGenerator(
            self.cat,
            self.words,
            name_dob_combo,
            self.encryption_dict,
            self.substitutors_dict).process_individual()

        return name_dob_combo

    def date_and_name_processor(self, name, dob):
        """
        Date and Name processor
        """
        name_dob = []
        name_dob.append(name + str(dob))
        name_dob.append(name + str(dob.year))
        name_dob.append(str(dob.year) + name)
        name_dob.append(str(dob.year)[2] + str(dob.year)[3] + name)
        name_dob.append(name + str(dob.year)[2] + str(dob.year)[3])

        return name_dob
