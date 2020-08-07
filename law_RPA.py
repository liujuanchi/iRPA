import tagui as t
import os
import datetime

MAX_WAIT = 30

def history_data_daily(url_prefix):
    t.init()  #
    init_url = url_prefix + '1.html'
    t.url(init_url)  # 初始url
    t.wait(15)  # 启动很慢
    max_page = int(t.read(element_identifier='//td[@class = "Normal"]').split('/')[1]) + 1  # 最大page数量
    for page_num in range(1, max_page):
        t.url(url_prefix + str(page_num) + '.html')
          # 启动很慢
        t.wait(5)
        print("现在所在页面 {}".format(page_num))

        # 拿到value
        count_values = t.count(element_identifier='//td[@colspan = "2"]//table') + 1
        today = datetime.datetime.today()
        today = str(today.date())
        # today = '2018-04-24'
        if t.read(element_identifier='//td[@colspan = "2"]//table[1]//span[@class = "hui12"]') < today:
            print("今日无增量")
            break
        print("页面有{}个文件".format(count_values - 1))

        for i in range(1, count_values):
            t.url(url_prefix + str(page_num) + '.html')
              # 启动很慢
            if t.read(element_identifier='//td[@colspan = "2"]//table['+str(i)+']//span[@class = "hui12"]') < today:
                t.close()
                exit(1)
            file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']')
            file_name = file_name[:-10] + str("_") + file_name[-10:] + str('.txt')
            time = file_name[-14:-4]
            prefix = 'http://www.pbc.gov.cn'
            content_url = prefix + t.read(
                element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')
            if '.html' not in t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href'):
                # 当直接跳到需要下载的文件的时候
                if 'cnhttp' in content_url:
                    content_url = content_url[21:]  # 不知道为什么会出错这个
                    # 取到数据
                    print("文件{} 是直接下载文件。".format(i))
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
                        if total_seconds > 30:
                            print('download fails')
                            break

                    os.rename(file_name, file_name[:-(len(suffix)+1)] + "_" + time +'.'+file_name[-(len(suffix)+1):])
                else:
                    # 取到数据
                    print("文件{} 是直接下载文件。".format(i))
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
                        if total_seconds > 30:
                            print('download fails')
                            break
                    os.rename(file_name, file_name[:-(len(suffix)+1)] + "_" + time +'.'+file_name[-(len(suffix)+1):])

            else:  # 当没有直接下载的时候
                if 'cnhttp' in content_url:
                    content_url = content_url[21:]  # 不知道为什么会出错这个
                    t.url(content_url)
                      # 启动很慢
                else:
                    t.url(content_url)
                      # 启动很慢
                # 获取pdf的数量，pdf的名字和pdf应该有的名字
                pdf_count = t.count(element_identifier='//div[@id = "zoom"]//a/@href')
                if pdf_count == 0:  ##如果是正常的txt文件
                    # 取到列表
                    print("文件{} 是文档。".format(i))
                    # 取text
                    if t.read(element_identifier='//div[@id = "zoom"]') != '':
                        text = t.read(element_identifier='//div[@id = "zoom"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    elif t.read(element_identifier='//td[@class = "p1"]') != '':
                        text = t.read(element_identifier='//td[@class = "p1"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    else:
                        with open('wrong_log.txt', 'a',encoding = 'utf-8') as f:
                            string = 'page {} doc {} didnt write in '.format(page_num,i)
                            f.write(string)
                        print("write files fails...")
                else:
                    # 取text
                    if t.read(element_identifier='//div[@id = "zoom"]') != '':
                        text = t.read(element_identifier='//div[@id = "zoom"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    elif t.read(element_identifier='//td[@class = "p1"]') != '':
                        text = t.read(element_identifier='//td[@class = "p1"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    else:
                        with open('wrong_log.txt', 'a',encoding = 'utf-8') as f:
                            string = 'page {} doc {} didnt write in '.format(page_num,i)
                            f.write(string)
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

                                if t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a') != '':
                                    #如果取到了
                                    print("这个p有!")
                                    pdf_name = t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href')
                                    # 取合规名
                                    pdf_name_to_change = t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a')
                                    # 下载
                                    suffix = pdf_name.split('.')[-1]

                                    pdf_name = pdf_name.split('/')[-1]
                                    prefix = 'http://www.pbc.gov.cn'
                                    download_link = prefix + t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href')
                                    if 'cnhttp' in download_link:
                                        t.url(t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href'))
                                          # 启动很慢
                                    else:
                                        t.url(download_link)
                                          # 启动很慢
                                    wait_seconds = 1
                                    total_seconds = 0
                                    while os.path.exists(pdf_name) == False:
                                        t.wait(wait_seconds)
                                        total_seconds += wait_seconds
                                        if total_seconds > 30:
                                            print('download fails')
                                            break
                                    os.rename(pdf_name, pdf_name_to_change)  # 改名
                                    os.rename(pdf_name_to_change,
                                              pdf_name_to_change[:-(len(suffix)+1)] + '_' + time + pdf_name_to_change[-(len(suffix)+1):])
                                    t.url(content_url)  # 返回二级目录
                                      # 启动很慢
                                    current_count += 1
                                    break
                                else:
                                    current_count += 1
                                    print("这个p没有")

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
                                with open(file_name, 'w',encoding = 'utf-8') as f:
                                    f.write(text)
                            elif t.read(element_identifier='//td[@class = "p1"]') != '':
                                text = t.read(element_identifier='//td[@class = "p1"]')
                                with open(file_name, 'w',encoding = 'utf-8') as f:
                                    f.write(text)
                            else:
                                with open('wrong_log.txt', 'a', encoding='utf-8') as f:
                                    str = 'page {} doc {} didnt write in '.format(page_num, i)
                                    f.write(str)
                                print("write files fails...")

    t.close()
    return 'execute success..'
def history_data(url_prefix):
    t.init()  #
    init_url = url_prefix + '1.html'
    t.url(init_url)  # 初始url
    t.wait(15) #启动很慢
    max_page = int(t.read(element_identifier='//td[@class = "Normal"]').split('/')[1]) + 1  # 最大page数量
    for page_num in range(1, max_page):
        t.url(url_prefix + str(page_num) + '.html')
        print("现在所在页面 {}".format(page_num))
        t.wait(5)
        # 拿到value
        count_values = t.count(element_identifier='//td[@colspan = "2"]//table') + 1
        print("页面有{}个文件".format(count_values - 1))
        for i in range(1, count_values):
            t.url(url_prefix + str(page_num) + '.html')
              # 启动很慢
            file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']')
            file_name = file_name[:-10] + str("_") + file_name[-10:] + str('.txt')
            time = file_name[-14:-4]
            prefix = 'http://www.pbc.gov.cn'
            content_url = prefix + t.read(
                element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')
            if '.html' not in t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href'):
                # 当直接跳到需要下载的文件的时候
                if 'cnhttp' in content_url:
                    content_url = content_url[21:]  # 不知道为什么会出错这个
                    # 取到数据
                    print("文件{} 是直接下载文件。".format(i))
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
                        if total_seconds > 30:
                            print('download fails')
                            break

                    os.rename(file_name, file_name[:-(len(suffix)+1)] + "_" + time +'.'+file_name[-(len(suffix)+1):])
                else:
                    # 取到数据
                    print("文件{} 是直接下载文件。".format(i))
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
                        if total_seconds > 30:
                            print('download fails')
                            break
                    os.rename(file_name, file_name[:-(len(suffix)+1)] + "_" + time +'.'+file_name[-(len(suffix)+1):])

            else:  # 当没有直接下载的时候
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
                            with open(file_name, 'w',encoding = 'utf-8') as f:
                                f.write(text)
                        except:
                            with open('实施《全国企业兼并破产和职工再就业工作计划》银行呆、坏帐准备金核销办法_1997-10-01.txt', 'w',encoding = 'utf-8') as f:
                                f.write(text)
                    elif t.read(element_identifier='//td[@class = "p1"]') != '':
                        text = t.read(element_identifier='//td[@class = "p1"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    else:
                        with open('wrong_log.txt', 'a',encoding = 'utf-8') as f:
                            string = 'page {} doc {} didnt write in '.format(page_num,i)
                            f.write(string)
                        print("write files fails...")
                else:
                    # 取text
                    if t.read(element_identifier='//div[@id = "zoom"]') != '':
                        text = t.read(element_identifier='//div[@id = "zoom"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    elif t.read(element_identifier='//td[@class = "p1"]') != '':
                        text = t.read(element_identifier='//td[@class = "p1"]')
                        with open(file_name, 'w',encoding = 'utf-8') as f:
                            f.write(text)
                    else:
                        with open('wrong_log.txt', 'a',encoding = 'utf-8') as f:
                            string = 'page {} doc {} didnt write in '.format(page_num,i)
                            f.write(string)
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

                                if t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a') != '':
                                    #如果取到了
                                    print("这个p有!")
                                    pdf_name = t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href')
                                    # 取合规名
                                    pdf_name_to_change = t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a')
                                    # 下载
                                    suffix = pdf_name.split('.')[-1]

                                    pdf_name = pdf_name.split('/')[-1]
                                    prefix = 'http://www.pbc.gov.cn'
                                    download_link = prefix + t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href')
                                    if 'cnhttp' in download_link:
                                        t.url(t.read(element_identifier='//div[@id = "zoom"]//p[last()-' + str(current_count) + ']//a/@href'))
                                          # 启动很慢
                                    else:
                                        t.url(download_link)
                                          # 启动很慢
                                    wait_seconds = 1
                                    total_seconds = 0
                                    while os.path.exists(pdf_name) == False:
                                        t.wait(wait_seconds)
                                        total_seconds += wait_seconds
                                        if total_seconds > 30:
                                            print('download fails')
                                            break
                                    os.rename(pdf_name, pdf_name_to_change)  # 改名
                                    os.rename(pdf_name_to_change,
                                              pdf_name_to_change[:-(len(suffix)+1)] + '_' + time + pdf_name_to_change[-(len(suffix)+1):])
                                    t.url(content_url)  # 返回二级目录
                                      # 启动很慢
                                    current_count += 1
                                    break
                                else:
                                    current_count += 1
                                    print("这个p没有")

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
                                with open(file_name, 'w',encoding = 'utf-8') as f:
                                    f.write(text)
                            elif t.read(element_identifier='//td[@class = "p1"]') != '':
                                text = t.read(element_identifier='//td[@class = "p1"]')
                                with open(file_name, 'w',encoding = 'utf-8') as f:
                                    f.write(text)
                            else:
                                with open('wrong_log.txt', 'a', encoding='utf-8') as f:
                                    str = 'page {} doc {} didnt write in '.format(page_num, i)
                                    f.write(str)
                                print("write files fails...")

    t.close()
    return 'execute success..'
def remove(path):
    filearray = []
    address_Excel=path
    f_list = os.listdir(address_Excel)
    for fileNAME in f_list:
    # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(fileNAME)[1] == '.pdf' or os.path.splitext(fileNAME)[1] == '.docx' or os.path.splitext(fileNAME)[1] == '.doc':
            filearray.append(fileNAME)
    # 以上是从pythonscripts文件夹下读取所有excel表格，并将所有的名字存储到列表filearray
    # print("在默认文件夹下有%d个文档" % len(filearray))
    ge = len(filearray)

    for i in range(ge):
        fname = filearray[i]
        os.remove(str(path)+'/'+str(fname))
    return 'remove  successful'



law_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144951/21885/index'
status = history_data(law_url)
print(status)
admin_law = 'http://www.pbc.gov.cn/tiaofasi/144941/144953/21888/index'
status = history_data(admin_law)
print(status)
compliance_url = 'http://www.pbc.gov.cn/tiaofasi/144941/3581332/3b3662a6/index'
status = history_data(compliance_url)
print(status)
regulation_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144957/21892/index'
status = history_data(regulation_url)
print(status)
other_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144959/21895/index'
status = history_data(other_url)
print(status)
# print(remove('/Users/maoyuanq/Desktop/规范性文件'))