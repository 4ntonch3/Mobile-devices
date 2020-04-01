# Information
**lab1.py** is a python script or a *wrapper* over the class **Billing**.

The realization of the class **Billing** is located in the folder *lib* in the root directory of the project.  

Requires python3 and following libraries:
+ json
+ os
+ sys  

These libraries should be installed with python3 packages.
# Usage
Script gets 3 parameters:
+ <terms_file_name>  
    The terms of the tariff of the user. For now the file should be filled manually. Format of the file: .csv
+ <data_file_name>  
    CDR file. Format of the file: .csv
+ <phone_number>  
    Phone number to calculate a bill.

`python lab1.py <terms_file_name> <data_file_name> <phone_number>`

Example of usage according to my variant:  
`python lab1.py terms.csv data.csv 915783624`  
! python3 !