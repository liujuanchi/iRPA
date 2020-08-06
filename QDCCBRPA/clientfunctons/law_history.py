import tagui as t
import os

def history_data(url_prefix):
    t.init()
    init_url = url_prefix + '1.html'
    t.url(init_url)
    max_page = int(t.read(element_identifier='//td[@class = "Normal"]').split('/')[1]) + 1
    for page_num in range(1,max_page):
        #主页面
        t.url(url_prefix+str(page_num)+'.html')
        print("现在所在页面 {}".format(page_num))
        t.wait(5)
        #拿到value
        count_values = t.count(element_identifier='//td[@colspan = "2"]//table') + 1
        print("页面有{}个文件".format(count_values-1))
        t.wait(5)
        for i in range(1,count_values):
            t.url(url_prefix + str(page_num) + '.html')
            if '.html' in t.read(element_identifier='//td[@colspan = "2"]//table['+str(i)+']//a/@href'):
                #取到列表
                print("文件{} 是文档。".format(i))
                file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']') + str('.txt')
                prefix = 'http://www.pbc.gov.cn'
                content_url = prefix + t.read(
                    element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//td//a/@href')
                # 点击url
                if content_url == 'http://www.pbc.gov.cnhttp://www.pbc.gov.cn/goutongjiaoliu/113456/113469/3487563/index.html':
                    content_url = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/3487563/index.html' #不知道为什么会出错这个
                t.url(content_url)
                # 取text
                if t.read(element_identifier='//div[@id = "zoom"]') != '':
                    text = t.read(element_identifier='//div[@id = "zoom"]')
                    with open(file_name, 'w') as f:
                        f.write(text)
                elif t.read(element_identifier='//td[@class = "p1"]') != '':
                    text = t.read(element_identifier='//td[@class = "p1"]')
                    with open(file_name, 'w') as f:
                        f.write(text)
                else:
                    print("write files fails...")
            elif '.doc' in t.read(element_identifier='//td[@colspan = "2"]//table['+str(i)+']//a/@href'):
                # 取到数据
                print("文件{} 是下载doc。".format(i))
                file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href').split('/')[-1]
                prefix = 'http://www.pbc.gov.cn'
                content_url = prefix + t.read(element_identifier='//td[@colspan = "2"]//table['+str(i)+']//a/@href')
                t.url(content_url)
                wait_seconds = 1
                total_seconds = 0
                while os.path.exists(file_name) == False:
                    t.wait(wait_seconds)
                    total_seconds += wait_seconds
                    if total_seconds > 30:
                        print('download fails')
                        break
            else:
                print("unknown format..")
            print("爬好一次，返回页面 {}".format(page_num))
    #close out
    t.close()
def compliance_data(url_prefix):
    t.init() #
    init_url = url_prefix + '1.html'
    t.url(init_url) #初始url
    max_page = int(t.read(element_identifier='//td[@class = "Normal"]').split('/')[1]) + 1 #最大page数量
    for page_num in range(1,max_page):
        t.url(url_prefix + str(page_num) +'.html')
        print("现在所在页面 {}".format(page_num))
        t.wait(5)
        # 拿到value
        count_values = t.count(element_identifier='//td[@colspan = "2"]//table') + 1
        print("页面有{}个文件".format(count_values - 1))
        t.wait(5)
        for i in range(1,count_values):
            t.url(url_prefix + str(page_num) + '.html')
            file_name = t.read(element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']') + str('.txt')
            prefix = 'http://www.pbc.gov.cn'
            content_url = prefix + t.read(
                element_identifier='//td[@colspan = "2"]//table[' + str(i) + ']//a/@href')
            if 'cnhttp' in content_url:
                content_url = content_url[21:]  # 不知道为什么会出错这个
                t.url(content_url)
                text = t.read(element_identifier='//div[@id = "zoom"]')
                with open(file_name, 'w') as f:
                    f.write(text)
                print("文件{} 是文档。".format(i))
                continue
            t.url(content_url)  #进入二级目录

            #获取pdf的数量，pdf的名字和pdf应该有的名字
            t.wait(2)
            pdf_count = t.count(element_identifier='//div[@id = "zoom"]//a/@href')
            if pdf_count == 0: ##如果是正常的txt文件
                # 取到列表
                print("文件{} 是文档。".format(i))
                # 取text
                if t.read(element_identifier='//div[@id = "zoom"]') != '':
                    text = t.read(element_identifier='//div[@id = "zoom"]')
                    with open(file_name, 'w') as f:
                        f.write(text)
                elif t.read(element_identifier='//td[@class = "p1"]') != '':
                    text = t.read(element_identifier='//td[@class = "p1"]')
                    with open(file_name, 'w') as f:
                        f.write(text)
                else:
                    print("write files fails...")
            elif ('pdf' in t.read(element_identifier='//div[@id = "zoom"]//a/@href')):
                print("文件{} 含有 {} 个pdf。".format(i,pdf_count))
                pdf_count += 1 #python从0开始，所以至少有一个pdf count
                for j in range(1,pdf_count):
                    #取pdf的名字
                    if t.read(element_identifier='//div[@id = "zoom"]//p['+str(j)+']//a/@href') != '':
                        print("当前是第{}个pdf。。".format(j))
                        pdf_name = t.read(element_identifier='//div[@id = "zoom"]//p['+str(j)+']//a/@href').split('/')[-1]
                        #取合规名
                        pdf_name_to_change = t.read(element_identifier='//div[@id = "zoom"]//p['+str(j)+']//a')
                        #下载
                        prefix = 'http://www.pbc.gov.cn'
                        t.url(prefix + t.read(element_identifier='//div[@id = "zoom"]//p['+str(j)+']//a/@href'))
                        wait_seconds = 1
                        total_seconds = 0
                        while os.path.exists(pdf_name) == False:
                            t.wait(wait_seconds)
                            total_seconds += wait_seconds
                            if total_seconds > 30:
                                print('download fails')
                                break
                        os.rename(pdf_name,pdf_name_to_change) #改名
                        t.url(content_url) #返回二级目录
                    else:
                        print("不合规，当文档处理！不读了！！！")
                        # 取text
                        if t.read(element_identifier='//div[@id = "zoom"]') != '':
                            text = t.read(element_identifier='//div[@id = "zoom"]')
                            with open(file_name, 'w') as f:
                                f.write(text)
                        elif t.read(element_identifier='//td[@class = "p1"]') != '':
                            text = t.read(element_identifier='//td[@class = "p1"]')
                            with open(file_name, 'w') as f:
                                f.write(text)
                        else:
                            print("write files fails...")
                        t.url(url_prefix + str(page_num) + '.html')
                        break
            else:
                print("文件{} 含有 {} 个pdf。".format(i,pdf_count))
                print("含有其他format的href，当文档处理！不读了！！！")
                # 取text
                if t.read(element_identifier='//div[@id = "zoom"]') != '':
                    text = t.read(element_identifier='//div[@id = "zoom"]')
                    with open(file_name, 'w') as f:
                        f.write(text)
                elif t.read(element_identifier='//td[@class = "p1"]') != '':
                    text = t.read(element_identifier='//td[@class = "p1"]')
                    with open(file_name, 'w') as f:
                        f.write(text)
                else:
                    print("write files fails...")
                t.url(url_prefix + str(page_num) + '.html')
                break


if __name__ == '__main__':
    pass
    # law_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144951/21885/index'
    # history_data(law_url)
    # admin_law = 'http://www.pbc.gov.cn/tiaofasi/144941/144953/21888/index'
    # history_data(admin_law)
    # compliance_url = 'http://www.pbc.gov.cn/tiaofasi/144941/3581332/3b3662a6/index'
    # compliance_data(compliance_url)
    # regulation_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144957/21892/index'
    # compliance_data(regulation_url)
    # other_url = 'http://www.pbc.gov.cn/tiaofasi/144941/144959/21895/index'
    # compliance_data(other_url)


