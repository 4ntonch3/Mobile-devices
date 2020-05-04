# Information
**lab2.py** is a python script or a *wrapper* over the class **Tarrifing**.

The realization of the class **Tarrifing** is located in the folder *lib* in the root directory of the project.  

Requires python3 and following libraries for python3:
+ json
+ os
+ sys
+ matplotlib
+ datetime  

!!! Also requires **nfdump** utility

These libraries should be installed with python3 packages.
# Usage
Script gets 3 parameters:
+ <netflow_traffic_file>  
    File with traffic. Will be parsed with nfdump utility.
+ <terms_file_name>  
    The terms of the tariff of the user. For now the file should be filled manually. Format of the file: .csv

`python3 lab2.py <netflow_traffic_file> <terms_file_name>`

Example of usage according to my variant:  
`python3 lab2.py nfcapd.202002251200 terms.csv`  
! python3 !