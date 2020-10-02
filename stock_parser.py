"""
Project is now deprecated since stock website layout has changed
which renders the links and html parsing useless.
"""

import requests
import requests_toolbelt.adapters.appengine
from bs4 import BeautifulSoup
from pprint import pprint
import traceback


requests_toolbelt.adapters.appengine.monkeypatch()


def extract_info(attr_dict):
    """
    :param attr_dict:  {u'href': u'controller.php?action=view_stock_charts&StockCode=134', u'title': u'BCB HOLDINGS
     LIMITED (DELISTED)'}
    :return: stockCode: CompanyName
    """
    # print attr_dict
    identifier = 'StockCode='
    index1 = attr_dict['href'].find(identifier)
    stock_code = attr_dict['href'][index1 + len(identifier):]
    return stock_code, attr_dict['title']


def get_all_companies():
    r = requests.get('http://www.stockex.co.tt/controller.php?action=listed_companies')
    soup = BeautifulSoup(r.text, 'html.parser')

    # print soup

    company_list = {}
    content = soup.find(id="content")
    for each_p in content.find_all('a'):
        try:
            stock_code, company_name = extract_info(each_p.attrs)
            company_list[stock_code] = company_name
        except Exception as e:
            print str(e)
    return company_list


def get_company_info(stock_code):
    try:
        info_dict = {}
        url = 'http://www.stockex.co.tt/controller.php?action=view_stock_charts&StockCode=' + str(stock_code)
        print url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        tr = soup.find_all('tr')
        table = tr[9]
        col = table.find_all('td')
        info_dict["opening_price"] = col[0].string
        info_dict["closing_price"] = col[1].string
        info_dict["change"] = col[2].contents[0]

        table2 = tr[15]
        col2 = table2.find_all('td')
        info_dict["high"] = col2[0].string
        info_dict["low"] = col[1].string
        info_dict["high_52_week"] = col2[2].string
        info_dict["low_52_week"] = col2[3].string
        return info_dict
    except Exception as e:
        print traceback.format_exc()
        return None


def get_company_history(stock_code, start_date, end_date):
    """
    Make post request to: http://www.stockex.co.tt/controller.php?action=view_stock_history&StockCode=118
    Post parameters (x-www-form-urlencoded):
    StartDate: 10/12/2016
    EndDate: 10/15/2016
    :return:
    """
    url = 'http://www.stockex.co.tt/controller.php?action=view_stock_history&StockCode=' + str(stock_code)
    params = {'StartDate': start_date, 'EndDate': end_date}
    print url
    r = requests.post(url, data=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    tr = soup.find_all('table')
    table = tr[3].find_all('p')
    headers = table[0:5]
    data = table[5:]
    output_dict = {}
    for info in range(0, len(data), 5):
        output_dict[data[info].text.replace(u'\xa0', u'').strip()] = {
            'closing_quote': data[info + 1].text.replace(u'\xa0', u'').strip(),
            'change_dollar': data[info + 2].text.replace(u'\xa0', u'').strip(),
            'change_percent': data[info + 3].text.replace(u'\xa0', u'').strip(),
            'volume_traded': data[info + 4].text.replace(u'\xa0', u'').strip()
        }
    return output_dict

if __name__ == "__main__":
    pprint(get_all_companies())
    # pprint(get_company_info(106))
    # get_company_history(118, '10/18/2016', '10/27/2016')
