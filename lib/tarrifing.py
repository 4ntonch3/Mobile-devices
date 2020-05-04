import re
import json
import pylab # matplotlib
from datetime import datetime

class Tariffing:
    def __init__(self, data_file, terms_file):
        self.__data_file = data_file
        self.__data = []
        self.__terms_file = terms_file
        self.__terms = None
        self.__sum_traffic_src = 0
        self.__sum_traffic_dst = 0
        self.__graph_data = []

    
    def solve(self):
        self.__obtainInformation()
        return self.__calculateBill()


    def __parseTerms(self):
        ip_addr = None
        intervals = []
        with open(self.__terms_file, 'r') as f:
            header = f.readline().split(',')
            header[len(header) - 1] =  header[len(header) - 1][:-1]
            columns = len(header)
            while True:
                format_line = dict()
                line = f.readline()
                if not(line):
                    break
                splited_line = line.split(',')
                if splited_line[len(splited_line) - 1][-1] == '\n':
                    splited_line[len(splited_line) - 1] = splited_line[len(splited_line) - 1][:-1]
                ip_addr = splited_line[0]
                if columns != len(splited_line):
                    raise Exception('Bad format. Columns error.')
                for col in range(1, columns):
                    if splited_line[col] == 'inf':
                        format_line[header[col]] = '-1'
                    else:
                        format_line[header[col]] = splited_line[col]
                intervals.append(format_line)
        terms = {
            'ip_addr' : ip_addr,
            'intervals' : intervals
        }
        self.__terms = json.dumps(terms)


    def __parseData(self):
        mask_ip_addrs = '([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):[0-9 ]*->[ ]*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):[0-9]*'
        mask_traffic = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9 ]{1,}[ ]{1,}([0-9\.]{1,})[ M]{1,}([0-9]{1,})'
        mask_date = '([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3})'
        with open(self.__data_file, 'r') as f:
            f.readline()
            while True:
                template_dict = dict()
                line = f.readline()
                if not(line):
                    break
                try:
                    template_dict['ip_src'], template_dict['ip_dst'] = re.findall(mask_ip_addrs, line)[0][0], re.findall(mask_ip_addrs, line)[0][1]
                    template_dict['traffic_src'], template_dict['traffic_dst'] = re.findall(mask_traffic, line)[0][0], re.findall(mask_traffic, line)[0][1]
                    template_dict['date'] = re.findall(mask_date, line)[0]
                except:
                    continue
                self.__data.append(template_dict)


    def __obtainInformation(self):
        self.__parseTerms()
        self.__parseData()
        js_terms = json.loads(self.__terms)
        for line in self.__data:
            if line['ip_src'] == js_terms['ip_addr']:
                if '.' in line['traffic_src']:
                    self.__sum_traffic_src += float(line['traffic_src']) * 1024 * 1024
                    template_graph_data = {
                        'date' : line['date'],
                        'traffic' : float(line['traffic_src']) * 1024 * 1024
                    }
                    self.__graph_data.append(template_graph_data)
                else:
                    self.__sum_traffic_src += int(line['traffic_src'])
                    template_graph_data = {
                        'date' : line['date'],
                        'traffic' : int(line['traffic_src'])
                    }
                    self.__graph_data.append(template_graph_data)
            elif line['ip_dst'] == js_terms['ip_addr']:
                if '.' in line['traffic_dst']:
                    self.__sum_traffic_dst += float(line['traffic_dst']) * 1024 * 1024
                    template_graph_data = {
                        'date' : line['date'],
                        'traffic' : float(line['traffic_dst']) * 1024 * 1024
                    }
                    self.__graph_data.append(template_graph_data)
                else:
                    self.__sum_traffic_dst += int(line['traffic_dst'])
                    template_graph_data = {
                        'date' : line['date'],
                        'traffic' : int(line['traffic_dst'])
                    }
                    self.__graph_data.append(template_graph_data)


    def drawGraph(self):
        unique_graph_data = dict()
        for data in self.__graph_data:
            try:
                unique_graph_data[datetime.strptime(data['date'].split('.')[0], "%Y-%m-%d %H:%M:%S")] += data['traffic']
            except KeyError:
                unique_graph_data[datetime.strptime(data['date'].split('.')[0], "%Y-%m-%d %H:%M:%S")] = data['traffic']
        x = []
        y = []
        for key in unique_graph_data.keys():
            x.append(key)
            y.append(unique_graph_data[key])

        pylab.scatter(x,y)
        pylab.show()


    def __calculateBill(self):
        commulated_traffic = 0
        bill = 0
        js_terms = json.loads(self.__terms)
        for term in js_terms['intervals']:
            if int(term['top_limit']) > commulated_traffic >= int(term['bot_limit']) or int(term['top_limit']) == -1:
                if self.__sum_traffic_dst + self.__sum_traffic_src <= int(term['top_limit']) or int(term['top_limit']) == -1:
                    commulated_traffic += self.__sum_traffic_dst + self.__sum_traffic_src
                    bill += (self.__sum_traffic_dst + self.__sum_traffic_src) * float(term['price'])
                else:
                    commulated_traffic += int(term['top_limit'])
                    bill += int(term['top_limit']) * float(term['price'])
        bill /= 1024*1024
        return bill