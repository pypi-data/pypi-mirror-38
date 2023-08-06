# datagovuk

Interface to provide pandas `pd.DataFrame` objects for all the dataset and 
organisation metadata, and datasets themselves in the [data.gov.uk](https://data.gov.uk/) CKAN database.

## Quickstart

```python
import datagovuk as dgu

orgs = dgu.organisation_structure()
print(orgs.head())

rsc = dgu.resources()

# Fetch a dataset from data.gov.uk
organogram_reference = rsc[
    (rsc.format == 'CSV') &
    (rsc.name == 'organogram-uk-statistics-authority')
    ].iloc[0]

organogram = dgu.resource(organogram_reference)

print(organogram)


```
```
>>>                                       highlighted                         name                                parent                        title
>>> id
>>> 5ea7a4ac-7455-4ab4-8296-b6b600bf9b6e        False         cranfield-university  fc87db43-996f-442b-b4b2-60f0287a9e22         Cranfield University
>>> a42aa1ab-8fbf-4fdf-bbca-07570caa1cfb        False      university-of-edinburgh  fc87db43-996f-442b-b4b2-60f0287a9e22      University of Edinburgh
>>> fc87db43-996f-442b-b4b2-60f0287a9e22        False                    academics                                  None                    Academics
>>> 3a9d8dc4-4f45-4d48-928a-6e3f04449dba        False    crown-prosecution-service  b5dbc6b9-f976-4b78-8bab-2ac41e78ed38    Crown Prosecution Service
>>> 486b7bf1-77d8-4ef2-8722-eab1eaf19b2e        False  government-legal-department  b5dbc6b9-f976-4b78-8bab-2ac41e78ed38  Government Legal Department
```

## Methods

    - datagovuk.organisation_structure()
    - datagovuk.organisations_groups()
    - datagovuk.organisations_users()
    - datagovuk.organisations()
    - datagovuk.datasets
