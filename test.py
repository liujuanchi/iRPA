import rpa_daily_increment
import rpa_history_data_without_date
import rpa_history_data
#import upload_s3
import os

file_name = rpa_daily_increment.main()
#flag = upload_s3.upload_to_aws_s3(file_name,'storageforrpa',file_name)
#if flag == True:
    #os.remove(file_name)

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
