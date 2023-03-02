from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from sqlalchemy.orm import Session

class DataExtract:

    def __init__(self,**kwargs):
        self.base_url = kwargs.get('base_url')
        

    def _collect_data(self,base_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        base_url = 'https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(base_url)
        page_source = driver.page_source
        soup = bs(page_source ,'html.parser')
        data = soup.find_all('tr', {'class':'tdcolumn'},recursive=True)
        print(len(data))
        flag=0

        base_data_collection = []
        for i in data:
            temp_data = {}
            row = i.find_all('td')
            if len(row)==7:
                temp_data['date'] =row[0].get_text()
                temp_data['security_code'] = row[1].get_text()
                temp_data['security_name'] = row[2].get_text()
                temp_data['client_name'] = row[3].get_text()
                temp_data['deal_type'] = row[4].get_text()
                temp_data['quantity'] = row[5].get_text()
                temp_data['price'] = row[6].get_text()
                base_data_collection.append(temp_data)
                flag=1

        if base_data_collection:
            context = {
                'flag':flag,
                'base_data_collection':base_data_collection
                }
    
        return context
        


