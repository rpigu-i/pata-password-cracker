import yaml 


class ProcessInputYaml():

    socialdata = {}

    def input_processor(self, yamldoc):

        opendoc = open(yamldoc, "r")
        self.socialdata = yaml.safe_load_all(opendoc)
        return self.socialdata
                
