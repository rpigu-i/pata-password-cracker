from patalib import Antonym, Synonym, Syzygy, Anomaly, Clinamen


class PasswordGenerator:

    bio_data = {}
    key = ""
    password_mappings = {}
    encryption_dict = {}
    substitutors_dict = {}
    words = []

    def __init__(
            self,
            key,
            words,
            bio_data,
            encryption_dict,
            substitutors_dict):
        """
        Store list of biographical data
        """
        self.key = key
        self.words = words
        self.bio_data = bio_data
        self.encryption_dict = encryption_dict
        self.substitutors_dict = substitutors_dict

    def process_individual(self):
        """
        Process an individuals data
        to generate a list of potential
        passwords
        """
        individual = {}
        count = 0
        for k, v in self.bio_data.iteritems():
            individual[self.key] = k
            if not isinstance(v, list):
                individual[k] = self.gen_pata_data(str(v))
            else:
                list_vals_to_process = []
                for listval in v:
                    list_vals_to_process.append(
                        self.gen_pata_data(str(listval)))
                individual[k] = list_vals_to_process

        return individual

    def gen_pata_data(self, bio_val):
        """
        Generate Pata Data
        """
        pata_data = []
        pata_data.append({'original': bio_val})
        pata_data.append(self.synonyms(bio_val))
        pata_data.append(self.antonym(bio_val))
        pata_data.append(self.syzygy(bio_val))
        pata_data.append(self.anomaly(bio_val))
        pata_data.append(self.clinamen(bio_val))

        return pata_data

    def gen_enc_list(self, clear_text):
        """
        Generate a list of encrypted
        items
        """
        encrypted = {}
        temp_enc_list = []

        for e in self.encryption_dict:
            for p in clear_text:
                temp_enc_list.append(self.encryption_dict[e]().hash(p))
            encrypted[e] = temp_enc_list
            temp_enc_list = []

        return encrypted

    def synonyms(self, bio_val):
        """
        Generate synonyms of input data
        """
        synonyms = Synonym().generate_synonym(bio_val)
        synonyms = list(set(synonyms['results']))
        new_synonyms = []
        clear_text = []
        encrypted = {}

        for i in synonyms:
            new_synonyms = new_synonyms + self.subsitutor(i)

        clear_text = list(set(new_synonyms + synonyms))
        encrypted = self.gen_enc_list(clear_text)

        return {'synonym': {'clear_text': clear_text, 'encrypted': encrypted}}

    def antonym(self, bio_val):
        """
        Generate antonyms of input data
        """
        antonyms = Antonym().generate_antonym(bio_val)
        antonyms = list(set(antonyms['results']))
        new_antonyms = []
        clear_text = []
        encrypted = {}

        for i in antonyms:
            new_antonyms = new_antonyms + self.subsitutor(i)

        clear_text = list(set(new_antonyms + antonyms))
        encrypted = self.gen_enc_list(clear_text)

        return {'antonyms': {'clear_text': clear_text, 'encrypted': encrypted}}

    def syzygy(self, bio_val):
        """
        Generate syzygy of input data
        """
        syzygys = Syzygy().generate_syzygy(bio_val)
        syzygys = list(set(syzygys['results']))
        new_syzygys = []
        clear_text = []
        encrypted = {}

        for i in syzygys:
            new_syzygys = new_syzygys + self.subsitutor(i)

        clear_text = list(set(new_syzygys + syzygys))
        encrypted = self.gen_enc_list(clear_text)

        return {'syzygys': {'clear_text': clear_text, 'encrypted': encrypted}}

    def anomaly(self, bio_val):
        """
        Generate anomaly of input data
        """
        anomalies = Anomaly().generate_anomaly(bio_val, self.words, 1)
        anomalies = list(set(anomalies['results']))
        new_anomalies = []
        clear_text = []
        encrypted = {}

        for i in anomalies:
            new_anomalies = new_anomalies + self.subsitutor(i)

        clear_text = list(set(new_anomalies + anomalies))
        encrypted = self.gen_enc_list(clear_text)

        return {
            'anomalies': {
                'clear_text': clear_text,
                'encrypted': encrypted}}

    def clinamen(self, bio_val):
        """
        Generate clinamen of input data
        """
        clinamen = Clinamen().generate_clinamen(bio_val, self.words, 1)
        clinamen = list(set(clinamen['results']))
        new_clinamen = []
        clear_text = []
        encrypted = {}

        for i in clinamen:
            new_clinamen = new_clinamen + self.subsitutor(i)

        clear_text = list(set(new_clinamen + clinamen))
        encrypted = self.gen_enc_list(clear_text)

        return {'clinamen': {'clear_text': clear_text, 'encrypted': encrypted}}

    def subsitutor(self, pwd):
        """
        Generate common character
        substitutions
        """
        new_pwds = []

        for s in self.substitutors_dict:
            generator_class = self.substitutors_dict[s]()
            new_pwds.append(generator_class.substitute(pwd))

        #mung_it = MungSubstitutor()
        # new_pwds.append(mung_it.total_mung_simple(pwd))
        # new_pwds.append(mung_it.random_mung_simple(pwd))

        return new_pwds
