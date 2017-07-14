from patalib import Antonym, Synonym, Syzygy, Anomaly, Clinamen
from subsitutor import MungSubstitutor

class PasswordGenerator:

    bio_data = {}
    password_mappings = {}

    def __init__(self, bio_data):
        """
        Store list of biographical data
        """
        self.bio_data = bio_data
        self.process_individual()
    

    def process_individual(self):
        """
        Process an individuals data 
        to generate a list of potential
        passwords
        """
        individual = {}
        count = 0
        for k, v in self.bio_data.iteritems():
            indv_key = str(count) +":" + k
            indv_key = indv_key.replace(" ", "")
            individual[indv_key] = k
            count = count + 1
            for bio in v.iteritems():
                individual[bio[0]] = self.gen_pata_data(str(bio[1]))

        print individual 
        print "--------------"

    def gen_pata_data(self, bio_val):
        """
        Generate Pata Data
        """
        pata_data = []
        pata_data.append({'original':bio_val})         
        pata_data.append(self.synonyms(bio_val))
        pata_data.append(self.antonym(bio_val))
        pata_data.append(self.syzygy(bio_val))

        return pata_data


    def synonyms(self, bio_val):
        """
        Generate synonyms of input data
        """
        synonyms = Synonym().generate_synonym(bio_val)
        synonyms = list(set(synonyms['results']))
        new_synonyms = []
        for i in synonyms:
            new_synonyms = new_synonyms + self.subsitutor(i)

        return {'synonym':list(set(new_synonyms+synonyms))}


    def antonym(self, bio_val):
        """
        Generate antonyms of input data
        """
        antonyms = Antonym().generate_antonym(bio_val)
        antonyms = list(set(antonyms['results']))
        new_antonyms = []
        for i in antonyms:
            new_antonyms = new_antonyms + self.subsitutor(i)

        return {'antonyms':list(set(new_antonyms+antonyms))}


    def syzygy(self, bio_val):
        """
        Generate syzygy of input data
        """
        syzygys = Syzygy().generate_syzygy(bio_val)
        syzygys = list(set(syzygys['results']))
        new_syzygys = []
        for i in syzygys:
            new_syzygys = new_syzygys + self.subsitutor(i)

        return {'syzygys':list(set(new_syzygys+syzygys))}


    def subsitutor(self, pwd):
        """
        Generate common character
        substitutions 
        """
        new_pwds = []
        mung_it = MungSubstitutor()
        new_pwds.append(mung_it.total_mung_simple(pwd))
        new_pwds.append(mung_it.random_mung_simple(pwd))
         
        return new_pwds


