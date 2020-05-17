# Information
**lab3.py** is a python script or a *wrapper* over the class **BillReceipt**.

The realization of the class **BillReceipt** is located in the folder *lib* in the root directory of the project.  

Requires python3 and following libraries for python3:
+ os
+ sys
+ argparse
+ docxtpl

These libraries should be installed with python3 packages.  

!!! Also requires **unoconv** utility  

Required commands:  
` sudo apt-get install unoconv `  
` pip3 install docxtpl `  

# Usage
To get .pdf receipt based on previous labs use:  
`python3 lab3.py --calculate --template_path <path_to_docx>`
+ <path_to_docx>  
    Docx template  

To create .pdf receipt with specified values use:
`python3 lab3.py --render --template_path <path_to_docx> --phone_bill <value_phone> --net_bill <value_net>`
+ <path_to_docx>  
    Docx template
+ <value_phone>  
    Float value
+ <value_net>  
    Float value

Example of usage according to my variant:  
`python3 lab3.py --calculate --template_path template.docx`  

Example of usage with arbitrary values:  
`python3 main.py --render --phone_bill 30.21 --net_bill 20.01  --template_path template.docx`  

! python3 !