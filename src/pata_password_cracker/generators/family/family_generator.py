from ..gen_password import PasswordGenerator 


class FamilyPasswordGenerator():

    family_data = {}
    cat = ""
    encryption_dict = {}

    def __init__(self, k, family_data, encryption_dict):
        """
        Grab family orientated
        data and process
        """

        self.family_data = family_data
        self.cat = k
        self.encryption_dict = encryption_dict


    def process_individual(self):
        """
        Process an individuals data 
        to generate a list of potential
        passwords
        """

        individual = {}
        pata_passwords = []

        for ind in self.family_data:
            for bio, values in ind.iteritems():
                pata_passwords.append(self.name_dob(bio, values))
                pata_passwords.append(PasswordGenerator(self.cat, values, self.encryption_dict).process_individual())
                individual[bio] = pata_passwords
                
            pata_passwords = []
       
        return individual

        

    def name_dob(self, bio, values):
        """
        Generate name/dob passwords.
        """
        name_dob_combo = {}


        if values['first_name'] and values['dob']:
            name_dob_combo['first_name_dob']  = \
                self.date_and_name_processor(values['first_name'], values['dob'])

        if values['last_name'] and values['dob']:
            name_dob_combo['last_name_dob']  = \
                self.date_and_name_processor(values['last_name'], values['dob'])

        name_dob_combo = PasswordGenerator(self.cat, name_dob_combo, self.encryption_dict).process_individual()
     
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
              

         
