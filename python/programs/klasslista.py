#!/usr/bin/env python3

import sys
import os
import csv
from dataclasses import dataclass


@dataclass
class contact:
    first_name: str = ""
    last_name: str = ""
    company_name: str = ""
    address: str = ""
    city: str = ""
    county: str = ""
    state: str = ""
    zip: str = ""
    phone1: str = ""
    phone: str = ""
    email: str = ""

    def csv(self):
        s = f'{self.first_name},{self.last_name},{self.company_name},'\
            f'{self.address},{self.city},{self.state},{self.zip},'\
            f'{self.phone1},{self.phone},{self.email}'
        return s

    def vcf(self):
        s = f'''BEGIN:VCARD
VERSION:3.0
N:{self.last_name};{self.first_name};;;
FN:{self.first_name} {self.last_name}
EMAIL;TYPE=INTERNET:{self.email}
TEL;TYPE=CELL:{self.phone}
CATEGORIES:Södertörns Friskola,MD_2021
TITLE:{self.company_name}
END:VCARD'''
        return s


csv_in = sys.argv[1]
contacts_csv = []


with open(csv_in) as cin:
    reader = csv.DictReader(cin)
    for row in reader:
        c1 = contact()
        c2 = contact()
        c1.company_name = \
            c2.company_name = ' '.join((row['kid_fn'], row['kid_ln']))
        name1 = row['parent1'].strip().split()
        if name1:
            c1.first_name = name1[0]
            c1.last_name = ' '.join(name1[1:])
        c1.email = row['mail1'].strip()
        c1.phone = row['phone1'].strip()
        c1.address = c2.address = row['address'].strip()
        name2 = row['parent2'].split()
        if name2:
            c2.first_name = name2[0]
            c2.last_name = ' '.join(name2[1:])
        c2.email = row['mail2'].strip()
        c2.phone = row['phone2'].strip()

        missing = True
        if c1.first_name and c1.email:
            contacts_csv.append(c1)
            missing = False
        if c2.first_name and c2.email:
            contacts_csv.append(c2)
            missing = False
        if missing:
            sys.stderr.write('Missing ' + c1.company_name + os.linesep)
            sys.stderr.flush()


for contact in contacts_csv:
    print(contact.vcf())
    print(contact.csv())
