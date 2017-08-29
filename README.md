# pata-password-cracker
Password cracker that implements patadata toolkit and other
metaphysical and psychological techniques.


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

Two fixed categories exist these being the core_data and family data. 
This is where a user core biographic data is stored, for example name, age, 
gender and so on. The family section contains family relationship data.
Specific processing is applied to this based upon known password
patterns.

This work has been inspired by Dr Helen Petrie and the ideas she defined in 
her work back in the early naughties.

Originally the plan was to use the four catgeories she defined as distinct 
subsections in the input YAML doc. However it was quickly discovered that
using the free_data category was just as effective for fans and fantasist 
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
python -m pata_password_cracker test_data.yaml words.txt
```

You should replace test_data.yaml with your input file containing
the data you wish to process.

words.txt should be replaced with a file/path containing a list of 
words, one per line.


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
core_bio data.

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

In the case of core_bio and famly data there are three specific reserved
fields, which are used for advanced processing. These are:

```
first_name
last_name
dob      
```

The dob should use a YYYY-MM-DD format.

In future versions, the list of reserved fields will
expand. 

The second section with advanced processing is the family section.
A family section is amde up of a lsit of individuals.

Each individual in the family section should therefore be included
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

As with the core_bio the three fields (dob, first_name and last_name) will
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

Currently all output is saved to a file called passwords.yaml.
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
Following this each category included e.g. core_bio, family, free_data
is listed.  
Under each category the key/value pairs and any advanced processing
that generates key/values in the fly is displayed. 

Following this each pataphysical category can be found e.g. synonym.
Within this category the password in clear text and encrypted formats
will then be enumerated.


## Encryption

Currently md5, SHA1, SHA224, SHA256, SHA384, and SHA512 are supported.
New encryption plugins can be added as needed.

In version 1 of the application all encryption formats are used.
Future versions of the software will allow filtering of this list.


## PataData

This is where the magic happens. Using pataphysical algorithms we can generate
all sorts of interesting password combinations based upon key value pairs.

You can read more about these at:

https://patamechanix.github.io/patalib/

This application uses version 1 of the packages and includes the following classes:

* Antonym
* Synonym
* Syzygy
* Clinamen
* Anomaly






