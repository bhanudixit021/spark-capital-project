from bs4 import BeautifulSoup as bs
import models
from datetime import datetime
import re
from selenium import webdriver

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--headless')
chrome_opt.add_argument('--no-sandbox')
chrome_opt.add_argument('--ignore-ssl-errors=yes')
chrome_opt.add_argument('--ignore-certificate-errors')

class DataExtract:

    def __init__(self,**kwargs):
        self.base_url = kwargs.get('base_url')
        self.driver = webdriver.Chrome(options=chrome_opt)
        

    def _collect_data(self,base_url,session):
        context = {"flag":0}
        try:
            self.driver.get(base_url)
            page_source = self.driver.page_source
            soup = bs(page_source ,'html.parser')
            data = soup.find_all('tr', {'class':'tdcolumn'},recursive=True)
            print(len(data))


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
                    print(temp_data)
            for data in base_data_collection:
                dataObject = models.BseData(
                    deal_date = datetime.strptime(data['date'],'%m/%d/%Y'),
                    security_code = data['security_code'],
                    security_name = data['security_name'],
                    client_name = data['client_name'],
                    deal_type = data['deal_type'],
                    quantity = data['quantity'],
                    price = float(re.sub(',','',data['price']))
                )
                session.add(dataObject)
                session.commit()
                session.refresh(dataObject)

            context['flag']=flag
            return context
        except:
            self.driver.close()
            context["flag"]=0
            return context
        finally:
            self.driver.close()
            context["flag"]=0
            return context
        


