import yaml


class ProcessInputYaml():
    """
    Class to take an input YAML file
    of key words. Opens it and returns it
    for processing
    """

    def yaml_processor(self, yamldoc):
        """
        Open the YAML doc and return to
        caller
        """
        socialdata = {}
        opendoc = open(yamldoc, "r")
        socialdata = yaml.safe_load_all(opendoc)
        return socialdata


class ProcessInputWords():
    """
    Class to take an input word list and process
    it for use in pataphysial algos
    """

    def words_processor(self, worddoc):
        """
        Process input word list
        """
        worddata = []
        with open(worddoc) as file:
            for line in file:
                worddata.append(line.strip())
        return worddata
