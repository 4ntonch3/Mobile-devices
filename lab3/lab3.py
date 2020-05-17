import argparse
import sys
import os
sys.path.append(os.path.abspath("../lib"))  
from billing import Billing
from tarrifing import Tariffing
from bill_receipt import BillReceipt


def calc_phone_bill():
    terms_file = '../lab1/terms.csv'
    cdr_file = '../lab1/data.csv'
    phone_number = '915783624'
    obj_bill = Billing(terms_file, cdr_file, phone_number)
    bill = obj_bill.getBill()
    if obj_bill.getError() is not None:
        print(obj_bill.getError())
        sys.exit()
    return bill


def calc_net_bill():
    traffic_file = '../lab2/nfcapd.202002251200'
    terms_file = '../lab2/terms.csv'
    os.system(f'nfdump -r {traffic_file} >> output.bin')
    obj = Tariffing('output.bin', terms_file)
    bill = obj.solve()
    os.system('rm output.bin')
    return round(bill, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates receipt from a template.")
    parser.add_argument('--calculate', action="store_true")
    parser.add_argument('--render', action="store_true")
    parser.add_argument('--template_path', action="store", required=True, type=str)
    parser.add_argument('--phone_bill', action="store", type=float)
    parser.add_argument('--net_bill', action="store", type=float)
    args = parser.parse_args()

    obj = BillReceipt(args.template_path)

    if args.calculate:
        bill_phone = calc_phone_bill()
        net_phone = calc_net_bill()
        info = {
            'customer': "Преподаватель университета ИТМО",
            'basis': "Документ №1 от 18.05.2020",
            'service_1': {
                'title': 'Услуги телефонной связи',
                'amount': 1,
                'price': bill_phone,
                'total': bill_phone
                },
            'service_2': {
                'title': 'Услуги по предоставлению интернет-соединения',
                'amount': 1,
                'price': net_phone,
                'total': net_phone
            }, 
        }
    elif args.render:
        info = {
            'customer': "Преподаватель университета ИТМО",
            'basis': "Документ №1 от 18.05.2020",
            'service_1': {
                'title': 'Услуги телефонной связи',
                'amount': '1',
                'price': args.phone_bill,
                'total': args.phone_bill
                },
            'service_2': {
                'title': 'Услуги по предоставлению интернет-соединения',
                'amount': '1',
                'price': args.net_bill,
                'total': args.net_bill
            }, 
        }
    obj.upload_info(info)
    obj.fill_doc_with_data('generated.docx')
    print('Check generated.docx')