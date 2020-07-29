http://www.pbc.gov.cn/tiaofasi/144941/144951/21885/index1.html

dump 中国人民银行国家法律 to 国家法律list.csv

for card from 1 to 20
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/font/a/@href to urltxt  
    
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/font/a/@title to titletxt  
    
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/span to datetxt
    dealrow = [titletxt + ", " + datetxt + ", http://www.pbc.gov.cn" + urltxt]

    write `csv_row(dealrow)` to 国家法律list.csv

click 下一页

for card from 1 to 20
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/font/a/@href to urltxt  
    
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/font/a/@title to titletxt  

    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/span to datetxt
    dealrow = [titletxt + ", " + datetxt + ", http://www.pbc.gov.cn" + urltxt]

    write `csv_row(dealrow)` to 国家法律list.csv

click 下一页


for card from 1 to 20
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/font/a/@href to urltxt  
    
    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/font/a/@title to titletxt  

    read ((//div[@class="portlet"]/div[2]/div[1]/table/tbody/tr[2]/td/table)[`card`])/tbody/tr/td[2]/span to datetxt
    dealrow = [titletxt + ", " + datetxt + ", http://www.pbc.gov.cn" + urltxt]

    write `csv_row(dealrow)` to 国家法律list.csv