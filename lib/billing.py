import json
import math

class Billing:
    def __init__(self, file_terms, file_billing, phone_number):
        self.__file_billing = file_billing
        self.__file_terms = file_terms
        self.__phone_number = phone_number
        self.__terms = None
        self.__data = None
        self.__bill = None
        self.__sms_count = None
        self.__in_minutes = None
        self.__error = None


    def getBill(self):
        self.__sms_count = 0
        self.__in_minutes = 0
        try:
            self.__calculateBill()
        except Exception as e:
            self.__error = str(e)
            return None
        return self.__bill


    def getError(self):
        return self.__error


    def __parseTermsCSV(self):
        in_calls = []
        out_calls = []
        sms = []
        with open(self.__file_terms, 'r') as f:
            header = f.readline().split(',')
            header[len(header) - 1] =  header[len(header) - 1][:-1]
            columns = len(header)
            while True:
                format_line = dict()
                line = f.readline()
                if not(line):
                    break
                splited_line = line.split(',')
                splited_line[len(splited_line) - 1] = splited_line[len(splited_line) - 1][:-1]
                service = splited_line[0]
                if columns != len(splited_line):
                    raise Exception('Bad format. Columns error.')
                for col in range(1, columns):
                    if splited_line[col] == 'inf':
                        format_line[header[col]] = '-1'
                    else:
                        format_line[header[col]] = splited_line[col]
                if service == 'in_calls':
                    in_calls.append(format_line)
                elif service == 'out_calls':
                    out_calls.append(format_line)
                elif service == 'sms':
                    sms.append(format_line)
                else: 
                    raise Exception('Wrong service.')
        terms = {
            'in_calls' : in_calls,
            'out_calls' : out_calls,
            'sms' : sms
        }
        self.__terms = json.dumps(terms)


    def __parseBillingCSV(self):
        data_list = []
        with open(self.__file_billing, 'r') as f:
            header = f.readline().split(',')
            header[len(header) - 1] =  header[len(header) - 1][:-1]
            while True:
                format_line = dict()
                line = f.readline()
                is_right_number = False
                if not(line):
                    break
                splited_line = line.split(',')
                for i in range(len(splited_line)):
                    format_line[header[i]] = splited_line[i]
                    if (header[i] == 'msisdn_origin' and splited_line[i] == self.__phone_number) or (header[i] == 'msisdn_dest' and splited_line[i] == self.__phone_number):
                        is_right_number = True
                if is_right_number:
                    format_line[header[len(header) - 1]] = format_line[header[len(header) - 1]][:-1]
                    data_list.append(json.dumps(format_line))
        for i in range(len(data_list) - 1):
            for j in range(i, len(data_list)):
                if json.loads(data_list[i])['timestamp'] > json.loads(data_list[j])['timestamp']:
                    data_list[i], data_list[j] = data_list[j], data_list[i]
        self.__data = data_list    


    def __calculateBill(self):
        self.__parseTermsCSV()
        self.__parseBillingCSV()
        in_calls_bill = 0
        out_calls_bill = 0
        sms_bill = 0
        js_terms = json.loads(self.__terms)
        for line in self.__data:
            js_line = json.loads(line)
            if js_line['msisdn_origin'] == self.__phone_number:
                sms_bill += self.__calcSms(int(js_line['sms_number']), js_terms['sms'])
                in_calls_bill += self.__calcCalls(js_line, js_terms['in_calls'])
            if js_line['msisdn_dest'] == self.__phone_number:
                out_calls_bill += self.__calcCalls(js_line, js_terms['out_calls'])
        self.__bill = sms_bill + in_calls_bill + out_calls_bill


    def __calcSms(self, amount, sms_terms):
        bill = 0
        for term in sms_terms:
            if int(term['bot_limit']) <= self.__sms_count < int(term['top_limit']) or (int(term['bot_limit']) <= self.__sms_count and int(term['top_limit']) == -1):
                if int(term['top_limit']) == -1 or int(term['top_limit']) - self.__sms_count >= amount:
                    bill += amount * int(term['price'])
                    self.__sms_count += amount
                else:
                    bill += (int(term['top_limit']) - self.__sms_count) * int(term['price'])
                    amount -= (int(term['top_limit']) - self.__sms_count)
                    self.__sms_count += (int(term['top_limit']) - self.__sms_count)
        return bill


    def __calcCalls(self, line, in_terms):
        bill = 0
        for term in in_terms:
            if term['bot_time'] <= line['timestamp'].split(' ')[-1] < term['top_time']:
                if int(term['bot_limit']) <= self.__in_minutes and (self.__in_minutes < int(term['top_limit']) or int(term['top_limit']) == -1):
                    if float(line['call_duration']) > float(term['top_limit']) - self.__in_minutes and int(term['top_limit']) != -1:
                        bill += (int(term['top_limit']) - self.__in_minutes) * int(term['price'])
                        line['call_duration'] = str(round((float(line['call_duration']) - float(term['top_limit']) + self.__in_minutes)))
                        self.__in_minutes = float(term['top_limit'])
                    else:
                        bill += math.ceil(float(line['call_duration'])) * int(term['price'])
                        self.__in_minutes += float(line['call_duration'])
        return bill        
