import argparse
from input import ProcessInputYaml
from gen_logo import Logo
from gen_password import PasswordGenerator 

def main():
    """
    Function to kick off the show.
    Accepts a YAML file as input
    """

    logo = Logo()
    logo.generate_logo()
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml", help="an input YAML doc of bio and geographical data of the target")
    args = parser.parse_args()
    process_input(args.yaml)


def process_input(file):
    """
    Create a new YAML parsing object
    and dump the content out as a dict
    """
 
    print "Processing input YAML"
    yaml_to_dict = ProcessInputYaml()
    yaml_to_dict = yaml_to_dict.input_processor(file)
    
    for i in yaml_to_dict:
        for x in i['individuals']:
            generate_password_list(x)


def generate_password_list(individual):
    """
    Kick off the password list generation
    """
    individuals_passwords = PasswordGenerator(individual)
        
            

if __name__ == "__main__":
    main()

