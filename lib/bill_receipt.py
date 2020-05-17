from docxtpl import DocxTemplate
from datetime import datetime
from numtotext import decimal2text
import os
import decimal

BIK_LEN = len('048965752')
BANK_ACCOUNT_LEN = len('4587996129846528')
INN_LEN = len('8979461395')
KPP_LEN = len('8795619852')
MONTH = {
    '1': 'января',
    '2': 'февраля',
    '3': 'марта',
    '4': 'апреля',
    '5': 'мая',
    '6': 'июня',
    '7': 'июля',
    '8': 'августа',
    '9': 'сентября',
    '10': 'октября',
    '11': 'ноября',
    '12': 'декабря',
}

class BillReceipt:
    def __init__(self, template_path):
        self.__doc = DocxTemplate(template_path)
        self.__context = dict.fromkeys(['bank', 'bik', 'bank_account', 'inn', 'kpp', 'recipient_account', 'recipient', 'num', 'day' ,'month' ,'year' ,'vendor' ,'customer' , 'basis', 'title_1' , 'title_2' , 'amount_1' ,'amount_2' ,'price_1' ,'price_2' ,'total_1' ,'total_2' ,'total_sum' ,'total_nds' ,'overall' ,'overall_text', 'director', 'accountant'])
        self.__js_info = None
        self.__requisites = {
            'bank': 'АО "СуперБанк" г. Санкт-Петербург',
            'bik': '048965752',
            'bank_account': '4587996129846528',
            'inn': '8979461395',
            'kpp': '8795619852',
            'recipient_account' : '8271937129217423',
            'recipient': 'ООО Лабораторная 3' 
        }
        self.__vendor = 'ООО Лабораторная 3'
        self.__counter = 1
        self.__accountant = 'Смирнова А.А.'
        self.__director = 'Челпанов А.Д.'


    def upload_info(self, js_info: dict):
        self.__js_info = self.__js_verify_info(js_info)


    def update_counter(self, num: int):
        self.__counter = num


    def update_requisites(self, new_js):
        if not self.__js_verify_requisites(new_js):
            print('Updating process crashed.')
            return 0
        for key, value in new_js.items():
            self.__requisites[key] = value


    def update_vendor(self, new_vendor: str):
        self.__vendor = new_vendor


    def update_accountant(self, new_accountant: str):
        self.__accountant = new_accountant


    def update_director(self, new_director: str):
        self.__director = new_director

    
    def fill_doc_with_data(self, new_path):
        self.__context['num'] = self.__counter
        if self.__js_info is None:
            print('Upload info with upload_info function')
            return 0
        try:
            self.__fill_info_table()
            self.__fill_data()
            self.__fill_contacts()
            self.__fill_table()
            self.__fill_table_sum()
        except Exception as e:
            print('Error during parsing info. Check input formats.')
            print(str(e))
        try:
            self.__doc.render(self.__context)
        except Exception as e:
            print('Error during rendering docs\'s template.')
            print(str(e))
        self.__doc.save(new_path)
        os.system(f'unoconv -fpdf {new_path} 2> /dev/null')
        os.system(f'rm {new_path}')
        self.__counter += 1


    def __js_verify_info(self, js):
        try:
            if len(js['customer']) < 3:
                print('Wrong "customer" field len.')
                return False
            if len(js['basis']) < 3:
                print('Wrong "basis" field len.')
                return False
            service_1, service_2 = js['service_1'], js['service_2']
            if len(service_1['title']) < 3:
                print('Wrong value of "title" field in service_1.')
                return False
            if len(service_2['title']) < 3:
                print('Wrong value of "title" field in service_2.')
                return False
            if int(service_1['amount']) < 0:
                print('Wrong value of "amount" field in service_1.')
                return False
            if int(service_2['amount']) < 0:
                print('Wrong value of "amount" field in service_2.')
                return False      
            if int(service_1['price']) < 0:
                print('Wrong value of "price" field in service_1.')
                return False 
            if int(service_2['price']) < 0:
                print('Wrong value of "price" field in service_2.')
                return False          
            if int(service_1['total']) < 0:
                print('Wrong value of "total" field in service_1.')
                return False 
            if int(service_2['total']) < 0:
                print('Wrong value of "total" field in service_2.')
                return False              
        except KeyError:
            print('One of the fields is missing.')
            return None
        except:
            return None
        return js


    def __js_verify_requisites(self, js):
        try:
            if len(js['bank']) < 3:
                print('Wrong "bank" field len.')
                return False
            if len(js['bik']) != BIK_LEN:
                print('Wrong "bik" field len.')
                return False
            if len(js['bank_account']) != BANK_ACCOUNT_LEN:
                print('Wrong "bank_account" field len.')
                return False
            if len(js['inn']) != INN_LEN:
                print('Wrong "inn" field len.')
                return False
            if len(js['kpp']) != KPP_LEN:
                print('Wrong "kpp" field len.')
                return False
            if len(js['recipient_account']) != BANK_ACCOUNT_LEN:
                print('Wrong "recipient_account" field len.')
                return False
            if len(js['recipient']) < 3:
                print('Wrong "recipient" field len.')
                return False
        except KeyError:
            print('One of the fields is missing.')
            return False
        return True
    

    def __fill_info_table(self):
        for key, value in self.__requisites.items():
            self.__context[key] = value


    def __fill_data(self):
        now = datetime.now()
        self.__context['day'] = now.day
        self.__context['month'] = MONTH[str(now.month)]
        self.__context['year'] = now.year % 100


    def __fill_contacts(self):
        self.__context['vendor'] = self.__vendor
        self.__context['customer'] = self.__js_info['customer']
        self.__context['basis'] = self.__js_info['basis']
        self.__context['director'] = self.__director
        self.__context['accountant'] = self.__accountant

    
    def __fill_table(self):
        service_1, service_2 = self.__js_info['service_1'], self.__js_info['service_2']
        for key in service_1.keys():
            self.__context[key+'_1'] = service_1[key]
            self.__context[key+'_2'] = service_2[key]


    def __fill_table_sum(self):
        self.__context['total_sum'] = self.__context['total_1'] + self.__context['total_2']
        self.__context['total_tax'] = round(self.__context['total_sum'] * 0.2, 2)
        self.__context['overall'] = self.__context['total_sum']
        self.__context['overall_text'] = decimal2text(
            decimal.Decimal(self.__context['overall']),
            int_units=((u'рубль', u'рубля', u'рублей'), 'm'),
            places=2,
            exp_units=((u'копейка', u'копейки', u'копеек'), 'f')
        ).capitalize() 


    def __fill_signatures(self):
        self.__context['director'] = self.__director
        self.__context['accountant'] = self.__accountant