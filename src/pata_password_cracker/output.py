import yaml


class ProcessOutputYaml():

    def output_processor(self, ind_dict):

        output_doc = file('passwords.yaml', 'w')
        yaml.dump(ind_dict, output_doc, default_flow_style=False)
