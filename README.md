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
using the free_data category was jsut as effective for fans and fantasist 
based results. 


## Command line 

The tool can be run as follows:


```
python -m pata_password_cracker test_data.yaml
```

## YAML format

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
        birthdate: 05/06/82
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


## Encryption

Currently md5, SHA1, SHA224, SHA256, SHA384, and SHA512 are supported.
New encryption plguins can be added as needed.


## PataData

This is where the magic happens. Using pataphysical algorithms we can generate
all sorts of interesting password combinations based upon key value pairs.


This is still in early stages of development......
 

