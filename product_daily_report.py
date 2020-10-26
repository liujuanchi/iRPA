import tagui as t
import datetime
import pandas as pd
import os
import s3_function

try:
    t.init()
    t.wait(5)
    #read page
    t.url("http://bank.jrj.com.cn/bankpro/")
    t.wait(5)
    #locate items
    item_list = t.read(element_identifier='//div[@class = "qutop mt"]').split()

    #txt
    today = datetime.datetime.today()
    today = str(today.date())
    file_name = today+'product_daily.txt'
    with open(file_name,'w',encoding='utf-8') as f:
        f.writelines([item+'\n' for item in item_list])
    #excel
    # daily_on_sale = int(item_list[1][:-11])
    # monthly_on_sale =int(item_list[2][:-13])
    # monthly_expire = int(item_list[3][:-13])
    #
    # pd.DataFrame({'今日在售银行理财产品':int(daily_on_sale),'本月累计发售银行理财产品':int(monthly_on_sale),'本月累计到期银行理财产品':int(monthly_expire)},index=[0]).to_csv(today+'product_daily.csv',index = False, encoding = 'utf-8')
    s3_function.upload_to_aws_s3(file_name,'s3qingdao',file_name)
    os.remove(file_name)
    t.close()
except:
    with open('FAIL_product_daily' + str((datetime.datetime.today()).date()) + '.txt', 'w', encoding='utf-8') as f:
        f.write("今日理财产品日报任务启动失败")
    s3_function.upload_to_aws_s3('FAIL_product_daily' + str((datetime.datetime.today()).date()) + '.txt', 's3qingdao',
                                 'FAIL_product_daily' + str((datetime.datetime.today()).date()) + '.txt')
    os.remove('FAIL_product_daily' + str((datetime.datetime.today()).date()) + '.txt')

