import tagui as t
import os
import datetime
import sys
import s3_function
import shutil

MAX_WAIT = 1000



def get_max_page(url_prefix):
    # 当达到max-page的最后一个count value文件index的时候，不用再做了。输出成功日志；进行下一个任务。。
    init_url = url_prefix + '1.html'
    t.url(init_url)  # 初始url
    max_page = int(t.read(element_identifier='//td[@class = "Normal"]').split('/')[1])  # 最大page数量
    with open('max_page_' + str(url_prefix.split('/')[-2]) + '.txt', 'w', encoding='utf-8') as f:
        f.write(str(max_page))
    return 'max_page_' + str(url_prefix.split('/')[-2]) + '.txt'


def get_count_values(page_num, url_prefix,today):
    t.url(url_prefix + str(page_num) + '.html')
    print("现在所在页面 {}".format(page_num))
    t.wait(5)
    # 拿到value
    count_values = t.count(element_identifier='//td[@colspan = "2"]//table')
    # today = '2018-04-24'
    if t.read(element_identifier='//td[@colspan = "2"]//table[1]//span[@class = "hui12"]') < today:
        return '今日无增量'
    print("页面有{}个文件".format(count_values))
    with open('count_items_' + str(page_num) + '_'+str(url_prefix.split('/')[-2]) + '.txt', 'w', encoding='utf-8') as f:
        f.write('page:' + str(page_num) + ':' + str(count_values))  # 以：为分隔符；记录当前页面和页面总共item数量
    return 'count_items_' + str(page_num) + '_'+str(url_prefix.split('/')[-2]) + '.txt'


def read_content(page_num, url_prefix, i,today):
    t.url(url_prefix + str(page_num) + '.html')
    # 启动很慢
    t.wait(2)
    if t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//span[@class = "hui12"]') < today:
        t.close()
        return '','','',''
    if '' == t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']'):
        print("no here")
        raise Exception("an exception")
    file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']')
    file_name = file_name[:-10] + str("_") + file_name[-10:] + str('.txt')
    time = file_name[-14:-4]
    prefix = 'http://www.pbc.gov.cn'
    content_url = prefix + t.read(
        element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')
    if '' == t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href'):
        print("no here")
        raise Exception("an exception")
    flag = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')  # 判断是否需要下载
    return flag, time, content_url, file_name


def direct_download(content_url, time, i):
    # 当直接跳到需要下载的文件的时候
    if 'cnhttp' in content_url:
        content_url = content_url[21:]  # 不知道为什么会出错这个
        # 取到数据
        print("文件{} 是直接下载文件。".format(i))
        if '' == t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href'):
            print("no here")
            raise Exception("an exception")

        file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')
        suffix = file_name.split('.')[-1]

        file_name = file_name.split('/')[-1]

        t.url(content_url)
        # 启动很慢
        wait_seconds = 1
        total_seconds = 0
        while os.path.exists(file_name) == False:
            t.wait(wait_seconds)
            total_seconds += wait_seconds
            if total_seconds > MAX_WAIT:
                print('download fails')
                break

        os.rename(file_name, file_name[:-(len(suffix) + 1)] + "_" + time + '.' + file_name[-(len(suffix) + 1):])
    else:
        # 取到数据
        print("文件{} 是直接下载文件。".format(i))
        if '' == t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href'):
            print("no here")
            raise Exception("an exception")

        file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')
        suffix = file_name.split('.')[-1]
        file_name = file_name.split('/')[-1]
        t.url(content_url)
        # 启动很慢
        wait_seconds = 1
        total_seconds = 0
        while os.path.exists(file_name) == False:
            t.wait(wait_seconds)
            total_seconds += wait_seconds
            if total_seconds > MAX_WAIT:
                print('download fails')
                break
        os.rename(file_name, file_name[:-(len(suffix) + 1)] + "_" + time + '.' + file_name[-(len(suffix) + 1):])


def read_text_content(content_url, file_name, page_num, i, time, url_prefix):
    # 读取网页

    if 'cnhttp' in content_url:
        content_url = content_url[21:]  # 不知道为什么会出错这个
        t.url(content_url)
        # 启动很慢
    else:
        t.url(content_url)
        # 启动很慢
    # 获取pdf的数量，pdf的名字和pdf应该有的名字
    t.wait(2)
    pdf_count = t.count(element_identifier='//div[@id = "zoom"]//a/@href')
    if pdf_count == 0:  ##如果是正常的txt文件
        # 取到列表
        print("文件{} 是文档。".format(i))
        # 取text
        if t.read(element_identifier='//div[@id = "zoom"]') != '':
            text = t.read(element_identifier='//div[@id = "zoom"]')
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(text)
            except:
                with open('实施《全国企业兼并破产和职工再就业工作计划》银行呆、坏帐准备金核销办法_1997-10-01.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
        elif t.read(element_identifier='//td[@class = "p1"]') != '':
            text = t.read(element_identifier='//td[@class = "p1"]')
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            with open('wrong_log.txt', 'a', encoding='utf-8') as f:
                string = 'page {} doc {} didnt write in '.format(page_num, i)
                f.write(string)
                f.write("\n")
            print("write files fails...")
    else:
        # 取text
        if t.read(element_identifier='//div[@id = "zoom"]') != '':
            text = t.read(element_identifier='//div[@id = "zoom"]')
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(text)
        elif t.read(element_identifier='//td[@class = "p1"]') != '':
            text = t.read(element_identifier='//td[@class = "p1"]')
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            with open('wrong_log.txt', 'a', encoding='utf-8') as f:
                string = 'page {} doc {} didnt write in '.format(page_num, i)
                f.write(string)
                f.write("\n")
            print("write files fails...")
        print("文件{} 含有 {} 个文件要下载。".format(i, pdf_count))
        pdf_count += 1  # python从0开始，所以至少有一个pdf count
        current_count = 0
        for j in range(1, pdf_count):
            # 取pdf的名字
            if '.htm' not in t.read(element_identifier='//div[@id = "zoom"]//p//a/@href'):
                print("当前是第{}个文件。。".format(j))
                p_count = t.count(element_identifier='//div[@id = "zoom"]//p')
                while current_count <= p_count:
                    try:
                        if t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(
                                current_count) + ']//a') != '':
                            # 如果取到了
                            print("这个p有!")
                            pdf_name = t.read(
                                element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href')
                            # 取合规名
                            pdf_name_to_change = t.read(
                                element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a')
                            # 下载
                            suffix = pdf_name.split('.')[-1]

                            pdf_name = pdf_name.split('/')[-1]
                            prefix = 'http://www.pbc.gov.cn'
                            download_link = prefix + t.read(
                                element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href')
                            if 'cnhttp' in download_link:
                                t.url(t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(
                                    current_count) + ']//a/@href'))
                                # 启动很慢
                            else:
                                t.url(download_link)
                                # 启动很慢
                            wait_seconds = 1
                            total_seconds = 0
                            while os.path.exists(pdf_name) == False:
                                t.wait(wait_seconds)
                                total_seconds += wait_seconds
                                if os.path.exists(pdf_name_to_change):
                                    break
                                if total_seconds > MAX_WAIT:
                                    print('download fails')
                                    with open('download_log.txt', 'a', encoding='utf-8') as f:
                                        string = 'page {} doc {} file {} didnt download '.format(page_num, i, j)
                                        f.write(string)
                                        f.write("\n")
                                    break
                            if os.path.exists(pdf_name_to_change):
                                pass
                            else:
                                os.rename(pdf_name, pdf_name_to_change)  # 改名
                                os.rename(pdf_name_to_change,
                                          pdf_name_to_change[:-(len(suffix) + 1)] + '_' + time + pdf_name_to_change[
                                                                                                 -(len(suffix) + 1):])
                            t.url(content_url)  # 返回二级目录
                            # 启动很慢
                            current_count += 1
                            break
                        else:
                            current_count += 1
                            print("这个p没有")
                    except:
                        print('some error occurs, nvm')
                        continue

            else:
                print("是个网页，当文档处理！")
                prefix = 'http://www.pbc.gov.cn'
                download_link = prefix + t.read(
                    element_identifier='//div[@id = "zoom"]//p[' + str(j) + ']//a/@href')
                if 'cnhttp' in download_link:
                    t.url(t.read(element_identifier='//div[@id = "zoom"]//p[' + str(j) + ']//a/@href'))
                    # 启动很慢
                else:
                    t.url(download_link)
                    # 启动很慢
                # 取text
                if t.read(element_identifier='//div[@id = "zoom"]') != '':
                    text = t.read(element_identifier='//div[@id = "zoom"]')
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(text)
                elif t.read(element_identifier='//td[@class = "p1"]') != '':
                    text = t.read(element_identifier='//td[@class = "p1"]')
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(text)
                else:
                    with open('wrong_log.txt', 'a', encoding='utf-8') as f:
                        string = 'page {} doc {} didnt write in '.format(page_num, i)
                        f.write(string)
                        f.write("\n")
                    print("write files fails...")


def history_data_daily(url_prefix, start_page=1):
    curr_page = 1
    curr_doc = 1
    today = datetime.datetime.today()
    today = str(today.date())
    try:
        t.init()
        page_file = get_max_page(url_prefix)
        with open(page_file, 'r') as f:
            max_page = int(f.read()) + 1  # 拿到最大page，加1因为python index是开区间；
        os.remove(page_file)
        for page_num in range(start_page, max_page):
            curr_page = page_num
            count_values_file = get_count_values(page_num, url_prefix,today)
            if count_values_file == '今日无增量':
                t.close()
                return True, '今日无增量'
            with open(count_values_file, 'r') as f:  # 拿到每一页的item数量；
                count_values = int(f.read().split(':')[-1]) + 1
            os.remove(count_values_file)
            for i in range(1, count_values):
                if os.path.exists('complete_log'+str(url_prefix.split('/')[-2])+'.txt'):
                    with open('complete_log' + str(url_prefix.split('/')[-2]) + '.txt', 'r') as f:
                        start_doc = f.read().split(',')[1]
                    if i < int(start_doc):
                        continue
                else:
                    pass
                curr_doc = i
                flag, time, content_url, file_name = read_content(page_num, url_prefix, i,today)
                if flag == '' and time == '' and content_url == '' and file_name == '':
                    t.close()
                    return True, '今日无增量'
                if '.html' not in flag:
                    # 当直接跳到需要下载的文件的时候：需要提供 当前url，time后缀，目前的文件index
                    direct_download(content_url, time, i)
                else:  # 当没有直接下载的时候,需要读取网页
                    # 读取网页
                    read_text_content(content_url, file_name, page_num, i, time, url_prefix)
            #顺利完成了item的循环，当前页完成，complete log翻页，start doc放在1;如果page_num已经是count - 1，就不用做事情了。
            if page_num != max_page - 1:
                with open('complete_log' + str(url_prefix.split('/')[-2]) + '.txt', 'w') as f:
                    f.write(str(page_num+1) + ',' + str(1))
            else:
                pass
        t.close()
        return True

    except: #如果检测到错误
        with open('complete_log' + str(url_prefix.split('/')[-2]) + '.txt', 'w') as f:
            f.write(str(curr_page) + ',' + str(curr_doc)) #留点
        t.close()
        return False


#/Users/maoyuanq/Desktop/
## C:/Users/Administrator/Desktop/
os.chdir('/Users/maoyuanq/Desktop')
if os.path.exists('/Users/maoyuanq/Desktop/daily'):
    # os.remove('C:/Users/Administrator/Desktop/daily')
    shutil.rmtree('/Users/maoyuanq/Desktop/daily')
os.mkdir('daily')
today = datetime.datetime.today()
today = str(today.date())

#test case 1.
iter_flag = False
law_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144951/21885/index'
os.chdir('/Users/maoyuanq/Desktop/daily/')
if os.path.exists('/Users/maoyuanq/Desktop/daily/law'):
    shutil.rmtree('/Users/maoyuanq/Desktop/daily/law')
    os.mkdir('law')
else:
    os.mkdir('law')
os.chdir('/Users/maoyuanq/Desktop/daily/law')
while iter_flag == False:
    if os.path.exists("complete_log" + str(law_url.split('/')[-2]) + ".txt"):  # 如果是中途断点
        with open("complete_log" + str(law_url.split('/')[-2]) + ".txt", 'r') as f:
            params = f.read().split(',')
            start_pag = int(params[0])
            iter_flag,message = history_data_daily(law_url, start_pag)
    else:  # 如果是首次运行
        iter_flag,message = history_data_daily(law_url, 1)

if message == '今日无增量':
    pass
else:
    os.remove("complete_log" + str(law_url.split('/')[-2]) + ".txt")
    #压缩文件，上传到云
    os.chdir('/Users/maoyuanq/Desktop/daily')
    s3_function.zip_ya('law')
    #upload
    s3_function.upload_to_aws_s3('law.zip','storageforccbrpa','law_daily'+today+'.zip')



#test case 2.
iter_flag = False
admin_law = 'http://www.pbc.gov.cn/tiaofasi/144941/144953/21888/index'
os.chdir('/Users/maoyuanq/Desktop/daily')
if os.path.exists('/Users/maoyuanq/Desktop/daily/admin'):
    shutil.rmtree('/Users/maoyuanq/Desktop/daily/admin')
    os.mkdir('admin')
else:
    os.mkdir('admin')
os.chdir('/Users/maoyuanq/Desktop/daily/admin')
while iter_flag == False:
    if os.path.exists("complete_log" + str(admin_law.split('/')[-2]) + ".txt"):  # 如果是中途断点
        with open("complete_log" + str(admin_law.split('/')[-2]) + ".txt", 'r') as f:
            params = f.read().split(',')
            start_pag = int(params[0])
            iter_flag,message = history_data_daily(admin_law, start_pag)
    else:  # 如果是首次运行
        iter_flag,message = history_data_daily(admin_law, 1)
if message == '今日无增量':
    pass
else:
    os.remove("complete_log" + str(admin_law.split('/')[-2]) + ".txt")
    #压缩文件，上传到云
    os.chdir('/Users/maoyuanq/Desktop/daily')
    s3_function.zip_ya('admin')
    #upload
    s3_function.upload_to_aws_s3('admin.zip','storageforccbrpa','admin_daily'+today+'.zip')

#test case 3.
iter_flag = False
compliance_url = 'http://www.pbc.gov.cn/tiaofasi/144941/3581332/3b3662a6/index'
os.chdir('/Users/maoyuanq/Desktop/daily/')
if os.path.exists('/Users/maoyuanq/Desktop/daily/compliance'):
    shutil.rmtree('/Users/maoyuanq/Desktop/daily/compliance')
    os.mkdir('compliance')
else:
    os.mkdir('compliance')
os.chdir('/Users/maoyuanq/Desktop/daily/compliance')
while iter_flag == False:
    if os.path.exists("complete_log" + str(compliance_url.split('/')[-2]) + ".txt"):  # 如果是中途断点
        with open("complete_log" + str(compliance_url.split('/')[-2]) + ".txt", 'r') as f:
            params = f.read().split(',')
            start_pag = int(params[0])
            iter_flag,message = history_data_daily(compliance_url, start_pag)
    else:  # 如果是首次运行
        iter_flag,message = history_data_daily(compliance_url, 1)
if message == '今日无增量':
    pass
else:
    os.remove("complete_log" + str(compliance_url.split('/')[-2]) + ".txt")
    #压缩文件，上传到云
    os.chdir('/Users/maoyuanq/Desktop/daily')
    s3_function.zip_ya('compliance')
    #upload
    s3_function.upload_to_aws_s3('compliance.zip','storageforccbrpa','compliance_daily'+today+'.zip')

#test case 4.
iter_flag = False
regulation_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144957/21892/index'
os.chdir('/Users/maoyuanq/Desktop/daily/')
if os.path.exists('/Users/maoyuanq/Desktop/daily/regulation'):
    shutil.rmtree('/Users/maoyuanq/Desktop/daily/regulation')
    os.mkdir('regulation')
else:
    os.mkdir('regulation')
os.chdir('/Users/maoyuanq/Desktop/daily/regulation')
while iter_flag == False:
    if os.path.exists("complete_log" + str(regulation_url.split('/')[-2]) + ".txt"):  # 如果是中途断点
        with open("complete_log" + str(regulation_url.split('/')[-2]) + ".txt", 'r') as f:
            params = f.read().split(',')
            start_pag = int(params[0])
            iter_flag,message = history_data_daily(regulation_url, start_pag)
    else:  # 如果是首次运行
        iter_flag,message = history_data_daily(regulation_url, 1)
if message == '今日无增量':
    pass
else:
    os.remove("complete_log" + str(regulation_url.split('/')[-2]) + ".txt")
    #压缩文件，上传到云
    os.chdir('/Users/maoyuanq/Desktop/daily')
    s3_function.zip_ya('regulation')
    #upload
    s3_function.upload_to_aws_s3('regulation.zip','storageforccbrpa','regulation_daily'+today+'.zip')


#test case 5.
iter_flag = False
other_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144959/21895/index'
os.chdir('/Users/maoyuanq/Desktop/daily/')
if os.path.exists('/Users/maoyuanq/Desktop/daily/others'):
    shutil.rmtree('/Users/maoyuanq/Desktop/daily/others')
    os.mkdir('others')
else:
    os.mkdir('others')
os.chdir('/Users/maoyuanq/Desktop/daily/others')
while iter_flag == False:
    if os.path.exists("complete_log" + str(other_url.split('/')[-2]) + ".txt"):  # 如果是中途断点
        with open("complete_log" + str(other_url.split('/')[-2]) + ".txt", 'r') as f:
            params = f.read().split(',')
            start_pag = int(params[0])
            iter_flag,message = history_data_daily(other_url, start_pag)
    else:  # 如果是首次运行
        iter_flag,message = history_data_daily(other_url, 1)
if message == '今日无增量':
    pass
else:
    os.remove("complete_log" + str(other_url.split('/')[-2]) + ".txt")
    #压缩文件，上传到云
    os.chdir('/Users/maoyuanq/Desktop/daily')
    s3_function.zip_ya('others')
    #upload
    s3_function.upload_to_aws_s3('others.zip','storageforccbrpa','others_daily'+today+'.zip')


# print(remove('/Users/maoyuanq/Desktop/规范性文件'))
