import sys
import os
sys.path.append(os.path.abspath("../lib"))  
from tarrifing import Tariffing


def displayUsage():
    print('\tUsage: ' + sys.argv[0] + ' <netflow traffic file> <terms_file_name>.\n')


def main():
    if len(sys.argv) != 3:
        print('Wrong amount of arguments.')
        displayUsage()
        return -1
    traffic_file, terms_file = sys.argv[1], sys.argv[2]

    os.system(f'nfdump -r {traffic_file} >> output.bin')
    obj = Tariffing('output.bin', terms_file)
    bill = obj.solve()
    print(f"Bill: {round(bill, 3)}")
    obj.drawGraph()
    os.system('rm output.bin')
    return 0

if __name__ == '__main__':
    sys.exit(main())