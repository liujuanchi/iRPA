import rpa_daily_increment
import rpa_history_data_without_date
import rpa_history_data
import s3_function as upload_s3
import os
import datetime
try:
    file_name = rpa_daily_increment.main()
    flag = upload_s3.upload_to_aws_s3(file_name,'s3qingdao',file_name)
    if flag == True:
        os.remove(file_name)
except:
    with open('rpa_daily' + str((datetime.datetime.today()).date()) + '.txt', 'w', encoding='utf-8') as f:
        f.write("今日理财日增数据拉取失败")
    upload_s3.upload_to_aws_s3('rpa_daily' + str((datetime.datetime.today()).date()) + '.txt', 's3qingdao',
                                 'rpa_daily' + str((datetime.datetime.today()).date()) + '.txt')
    os.remove('rpa_daily' + str((datetime.datetime.today()).date()) + '.txt')


#file_name = rpa_history_data_without_date.main()
#flag = upload_s3.upload_to_aws_s3(file_name,'storageforrpa',file_name)
#if flag == True:
#    os.remove(file_name)
#
#input = '2020'
#file_name = rpa_history_data.main(input)
#upload_s3.upload_to_aws_s3(file_name,'storageforrpa',file_name)
#if flag == True:
#    os.remove(file_name)
