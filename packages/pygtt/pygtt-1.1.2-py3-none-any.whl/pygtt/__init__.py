import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.5t.torino.it/5t/trasporto/arrival-times-byline.jsp?action=getTransitsByLine&shortName="

class PyGTT():

    def get_by_stop(self, stop):
        bus_list = []
        r = requests.get(BASE_URL+str(stop))
        soup = BeautifulSoup(r.text, 'html.parser')
        main_table = soup.findAll('table')[0]
        for row in main_table.findAll('tr'):
            bus = {}
            bus['time'] = []
            for column in row.findAll('td'):
                time = {}
                if column.findAll('a'):
                    bus['bus_name'] = column.find('a').text
                else:
                    if column.text:
                        run = column.text
                        if '*' not in column.text:
                            time['isRealtime'] = 'false'
                        else:
                            time['isRealtime'] = 'true'
                            run = column.text.replace('*', '')
                        time['run'] = run
                        bus['time'].append(time)
            bus_list.append(bus)
        return bus_list