# Pata Password Cracker 2.0
Password cracker that implements patadata toolkit and other
metaphysical and psychological techniques.

Version 2.x uses Python 3.x. For Python 2.x (deprecated) please 
refer to the v1 branch. 

## Introduction

This tools allows you to add an arbitary list of YAML key
value pairs to generate potential passwords from.

These would typically be biographical/georgraphical data
of the target. 

For example:

```
pet_name: biggles

hobby: football
```

The tool is agnostic so any key value pair you consider
worthy of attempting is valid. This is defined under the 
free data category.

Two fixed categories exist these being the `core_data` and family data. 
This is where a user core biographic data is stored, for example name, age, 
gender and so on. The family section contains family relationship data.
Specific processing is applied to this based upon known password
patterns.

This work has been inspired by Dr Helen Petrie and the ideas she defined in 
her work back in the early naughties.

Originally the plan was to use the four catgeories she defined as distinct 
subsections in the input YAML doc. However it was quickly discovered that
using the `free_data` category was just as effective for fans and fantasist 
based results. 


## Command line 

You can install the pata password cracking tool via pip:

```
pip install pata-password-cracker
```

After installation please download wordnet from
the NLTK downloader:
 
```
python -m nltk.downloader wordnet
```

The tool can then be run as follows:

```
python -m pata_password_cracker test_data.yaml words.txt md5,sha1
```

You should replace `test_data.yaml` with your input file containing
the data you wish to process.

words.txt should be replaced with a file/path containing a list of 
words, one per line.

Finally a list of types of encryption you want to output can be included.
Currently supported are: md5,sha1,sha256,sha384,sha512,bcrypt


## TOML and Poetry Support

This project now supports modern Python packaging with TOML configuration and Poetry dependency management.

### Using TOML Configuration

The project includes a `pyproject.toml` file that follows PEP 621 standards for project metadata. You can build the package using modern Python build tools:

```bash
# Install build tools
pip install build

# Build the package
python -m build
```

### Using Poetry

To use Poetry for dependency management and development:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install with development dependencies
poetry install --with dev

# Run the tool
poetry run python -m pata_password_cracker test_data.yaml words.txt md5,sha1

# Build the package
poetry build
```

### NLTK Dependencies

After installation, you need to install NLTK data. You can either:

1. Use the provided script:
```bash
python install_nltk_deps.py
```

2. Or install manually:
```bash
python -m nltk.downloader wordnet
```

### Development Dependencies

When using Poetry, the following development tools are included:
- pytest (testing)
- pytest-cov (coverage)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)


## YAML format

The input YAML file should use the following format:

```
individuals:
- James Smith:
    - core_bio:
        first_name: James
        last_name: Smith
        street1: 123
        street2: Broadway 
        city: New York
        zip: 0123
        dob: 1982-05-06
    - family:
        - individual_1: 
            relationship: father
            first_name: Tim
            last_name: Smith
            dob: 1945-12-21
        - individual_2: 
            relationship: mother  
            first_name: Susie
            last_name: Smith
            dob: 1944-03-03
    - free_data:
        pet1: cat
        pet1_name: ginger
        pet2: dog
        pet2_name: Tin Tin
        club: Masons
        lodge: Hermes
```

The first section that takes advanced processing is the
`core_bio` data.

```
- core_bio:
    first_name: James
    last_name: Smith
    street1: 123
    street2: Broadway 
    city: New York
    zip: 0123
    dob: 1982-05-06
```

In the case of `core_bio` and famly data there are three specific reserved
fields, which are used for advanced processing. These are:

```
first_name
last_name
dob      
```

The dob should use a `YYYY-MM-DD` format.

In future versions, the list of reserved fields will
expand. 

The second section with advanced processing is the family section.
A family section is made up of a list of individuals.

Each individual in the `family` section should therefore be included
using the following format:

```
- family:
  - individual_1: 
      relationship: father
      first_name: Tim
      last_name: Smith
      dob: 1945-12-21
  - individual_2: 
      relationship: mother  
      first_name: Susie
      last_name: Smith
      dob: 1944-03-03
```

As with the `core_bio` the three fields (dob, first_name and last_name) will
experience some advanced processing. Therefore each key/value should 
only be included once per individual.

## Words format

This is just a doc with a list 
of words. Linux and Unix-like operating systems often
include a words file. This can usually be found under:

```
/usr/share/dict/words
```

or

```
/usr/dict/words
```

If you wish to construct your own it should be a newline delimeted list.

For example:

```
Apple
Egg
Cabbage
Happy
Tree
Sun
Run
```

## Output

Currently all output is saved to a file called `passwords.yaml`.
Future versions of the software will allow the option to chose
the output file, and also output format.
For example XML or JSON.

The output is in the following example format:

```
0:JamesSmith:
  - core_bio:
    first_name_dob:
    - - original: James1982-06-05
      - synonym:
          clear_text:
          - J@m3$1982-06-05
          - JamesI982-06-05
          - James1982-06-05
          encrypted:
            bcrypt:
            - $2b$12$QCk59nMuLZ3oT0.H6cMBpunqs8QDlzYVsxuOYy09JvmrcDAHHy4eS
            - $2b$12$/bzGa1sqBWjzkriwxwpYa.dZIZ/Wg9Py.fuWI8DWoxE2mTiTzOIxK
            - $2b$12$pp.M7o4qiZibpB.JBP4WaOY11Ub1nTlHMNpj5peTHkmt26dhXe33m
            md5:
            - 92f32c3d9830a4b8be899ccf255d18aa
            - b2223c5713d5b684ed758214ee1668b9
            - 69ceebbe07cfac7fb1fc440ac55893d6
 
            ...

```

The output starts with a unqiue id for the target individual(s).
Following this each category included e.g. `core_bio`, `family`, `free_data`
is listed.  
Under each category the key/value pairs and any advanced processing
that generates key/values in the fly is displayed. 

Following this each pataphysical category can be found e.g. synonym.
Within this category the password in clear text and encrypted formats
will then be enumerated.


## Encryption

Currently md5, SHA1, SHA224, SHA256, SHA384, and SHA512 are supported.
New encryption plugins can be added as needed.

Add the encryption format you would like to the end of the command e.g.

```
python -m pata_password_cracker test_data.yaml words.txt sha1
```

Here SHA1 hashes will be included. Multiple formats can be added via comma
separation e.g. md5,sha1 etc. 


## PataData

This is where the magic happens. Using pataphysical algorithms we can generate
all sorts of interesting password combinations based upon key value pairs.

You can read more about these at:

https://github.com/rpigu-i/patalib

This application uses version 2 (Python 3 support) of the package and includes the following classes:

* Antonym
* Synonym
* Syzygy
* Clinamen
* Anomaly






