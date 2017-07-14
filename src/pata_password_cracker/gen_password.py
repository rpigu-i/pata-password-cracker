from patalib import Antonym, Synonym, Syzygy, Anomaly, Clinamen

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
        print self.bio_data
