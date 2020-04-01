import sys
import os
sys.path.append(os.path.abspath("../lib"))  
from billing import Billing

def displayUsage():
    print('\tUsage: ' + sys.argv[0] + ' <terms_file_name> <cdr_file_name> <phone_number>.\n')


def main():
    if len(sys.argv) != 4:
        print('Wrong amount of arguments.')
        displayUsage()
        return -1
    terms_file, cdr_file, phone_number = sys.argv[1], sys.argv[2], sys.argv[3]
    obj_bill = Billing(terms_file, cdr_file, phone_number)
    data = obj_bill.getBill()
    if obj_bill.getError() != None:
        print(obj_bill.getError())
        return -1
    print('Bill: ' + str(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())


# python .\lab1.py terms.txt data.csv 915783624