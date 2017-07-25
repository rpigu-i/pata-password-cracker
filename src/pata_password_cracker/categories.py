from gen_password import PasswordGenerator 
from family_generator import FamilyPasswordGenerator

class Categories:
    """
    Load categories from YAML
    representation.
    """  

    bio_data = {}
    password_mappings = {}
    individuals = {}

    def __init__(self, bio_data):
        """
        Store list of biographical data
        """
        self.bio_data = bio_data
        self.process_categories()
    

    def process_categories(self):
        """
        Process an individuals categories data 
        to generate a list of potential
        passwords
        """
        individual = {}
        count = 0
        for target in self.bio_data:
            indv_key = str(count) +":" + target
            indv_key = indv_key.replace(" ", "")
            individual[indv_key] = target
            target_vals = []
            count = count + 1   
            
 
            for category in self.bio_data[target]:
               for k, v in category.iteritems():
                   if k == 'core_bio' and v != None:
                       target_vals.append({k:self.process_core_bio(k,v)})
                   if k == 'family' and v != None:
                       target_vals.append({k:self.process_family(k,v)})
                   if k == 'fans' and v != None:
                       self.process_fans()
                   if k == 'fantasists' and v != None:
                       self.process_fans(v)
                   if k == 'crytpic' and v != None:
                       self.process_crytpic(v)
                   if k == 'free_data' and v != None:
                       self.process_free_data(v)
                   
            individual[indv_key] = target_vals
                   
        print individual 
        return individual


    def process_core_bio(self,k,core_bio_data):
        """
        Process the core bio data
        """
        bio_passwords = PasswordGenerator(k, core_bio_data).process_individual()
        return bio_passwords


    def process_family(self,k, family_bio_data):
        """
        Process the family bio data
        """
        family_passwords = FamilyPasswordGenerator(k, family_bio_data).process_individual()
        return family_passwords

    def process_fans(self, fans_bio_data):
        """
        Process the fans bio data
        """
        print "here"
 
    def process_fantasists(self, fantasists_bio_data):
        """
        Process the fantasists bio data
        """
        print "here"


    def process_cryptic(self, cryptic_bio_data):
        """
        Process the cryptic bio data
        """
        print "here"
     
    def process_free_data(self, free_data):
        """
        Process the context free bio data
        """
        print "here"
