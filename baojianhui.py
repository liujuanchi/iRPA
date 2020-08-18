#初始化
import tagui as t
import os
import traceback
import s3_function
MAX_WAIT = 1000

def web_init(web_url):
    t.url(web_url)
    t.wait(10)


def main_operation(url, mode = 'txt'):
    # 当前页面
    curr_page = int(t.read(element_identifier='//div[@class = "ng-binding"][last()]').split('/')[0])
    # 点击按钮
    list_count = t.count(element_identifier='//div[@class = "list caidan-right-list"]')  # 循环列表，取出总list有几个
    #如果是断点，读取断电数据
    if os.path.exists('baojianhui_log.txt'):
        with open('baojianhui_log.txt','r',encoding='utf-8') as f:
            params = f.read().split(',')
        curr_page = params[0]
        start_i = params[1]
        start_j = params[2]
    else: #如果是第一次执行，全取初始值；
        start_i = 1
        start_j = 1
    #常规操作
    for i in range(1, list_count + 1):
        t.wait(3)
        if i < int(start_i):
            continue
        item_count = t.count(
            element_identifier='//div[@class = "list caidan-right-list"][' + str(
                i) + ']//div[@class = "panel-row ng-scope"]')  # 取出每个list里的具体法规有几条
        print('当前是list {}, 里面的元素有 {} 个'.format(str(i), str(item_count)))
        t.wait(3)
        for j in range(1, item_count + 1):
            if j < int(start_j):
                continue
            item_title = t.read(element_identifier='//div[@class = "list caidan-right-list"][' + str(
                i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a')
            time_suffix = t.read(element_identifier='//div[@class = "list caidan-right-list"][' + str(
                i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//span[@class = "date ng-binding"]')
            file_name = item_title + '_' + time_suffix + '.txt'
            if '/' in file_name:
                file_name = file_name.replace('/',' ')
            if mode == 'txt':
                #点击
                link = t.read(element_identifier='//div[@class = "list caidan-right-list"]['+str(i)+']//div[@class = "panel-row ng-scope"]['+str(j)+']//a/@ng-href')
                prefix = 'http://www.cbirc.gov.cn/cn/view/pages/'
                final_link = prefix + link
                t.url(final_link)
                t.wait(1)
                while not os.path.exists(file_name):
                    type_1 = t.read(element_identifier='//div[@class = "Section0"]') + t.read(element_identifier='//div[@class = "Section1"]')
                    type_2 = t.read(element_identifier='//div[@class = "WordSection1"]')
                    type_3 = t.read(element_identifier='//div[@class = "wenzhang-content ng-binding"]')
                    if type_1 != '':
                        content = type_1
                        with open(file_name, 'w',encoding='utf-8') as f:
                            f.write(content)
                        break
                    elif type_2 != '':
                        content = type_2
                        with open(file_name, 'w',encoding='utf-8') as f:
                            f.write(content)
                        break
                    elif type_3 != '':
                        content = type_3
                        with open(file_name, 'w',encoding='utf-8') as f:
                            f.write(content)
                        break
                    else:
                        content = ' '
                        with open(file_name, 'w',encoding='utf-8') as f:
                            f.write(content)
                        break
            elif mode == 'doc':
                t.click(element_identifier='//div[@class = "list caidan-right-list"][' + str(
                    i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a[@ng-click = "fileDownload(x.docFileUrl)"]')
                doc_id = t.read(element_identifier='//div[@class = "list caidan-right-list"][' + str(
                    i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a/@ng-href').split('=')[1][:-7]
                doc_name = doc_id + '.doc'
                curr_clock = 5
                while not os.path.exists(doc_name):
                    t.wait(curr_clock)
                    curr_clock += 5
                    if curr_clock > MAX_WAIT:
                        break
                t.wait(2)
                os.rename(doc_name, item_title + '_' + time_suffix + '.doc')
            elif mode == 'pdf':
                t.click(element_identifier='//div[@class = "list caidan-right-list"][' + str(
                    i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a[@ng-click = "fileDownload(x.pdfFileUrl)"]')
                pdf_id = t.read(element_identifier='//div[@class = "list caidan-right-list"][' + str(
                    i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a/@ng-href').split('=')[1][:-7]
                pdf_name = pdf_id + '.pdf'
                curr_clock = 5
                while not os.path.exists(pdf_name):
                    t.wait(curr_clock)
                    curr_clock += 5
                    if curr_clock > MAX_WAIT:
                        break
                t.wait(2)
                os.rename(pdf_name, item_title + '_' + time_suffix + '.pdf')
            else:
                print('unknown format..')
                t.close()
                raise Exception("unknown input mode")
            # 返回主页面
            t.url(
                url + str(
                    curr_page))
            t.wait(2)
            with open('baojianhui_log.txt','w',encoding='utf-8') as f:
                f.write(str(curr_page) + ',' + str(i) + ',' + str(j))
        with open('baojianhui_log.txt','w',encoding='utf-8') as f:
            f.write(str(curr_page) + ',' + str(i) + ',' + str(1)) #当前list取完，j更新
    #循环完之后，翻页

def main(url, mode = 'txt'):
    if os.path.exists('baojianhui_log.txt'):
        with open('baojianhui_log.txt', 'r',encoding='utf-8') as f:
            params = f.read().split(',')
        curr_page = params[0]
    else:  # 如果是第一次执行，全取初始值；
        curr_page = 1
    url_link = str(url) + str(curr_page)
    web_init(url_link)
    total_page = int(t.read(element_identifier='//div[@class = "ng-binding"][last()]').split('/')[-1])
    while int(curr_page) < int(total_page): #从1开始，做完之后翻页；
        main_operation(url, mode) #如果有页可翻，就翻页
        print('click once')
        t.click(element_identifier='//a[@ng-click = "pager.next()"]') #翻页
        t.wait(5)
        curr_page = int(t.read(element_identifier='//div[@class = "ng-binding"][last()]').split('/')[0])
        with open('baojianhui_log.txt', 'w',encoding='utf-8') as f:
            f.write(str(curr_page) + ',' + str(1) + ',' + str(1)) #翻页之后，index重置；i更新；
    if curr_page == total_page:
        main_operation(url, mode) #如果是最后一页了，只需要做一次main
    t.close()
    return True


'C:/Users/Administrator/Desktop/wenjian'
os.chdir('C:/Users/Administrator/Desktop')
os.mkdir('../../Desktop/baojian_guizhang')
os.chdir('C:/Users/Administrator/Desktop/baojian_guizhang')
guizhang_flag = False
guizhang_url = 'http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=928&itemUrl=ItemListRightList.html&itemName=规章及规范性文件&itemsubPId=926#'
if os.path.exists('baojianhui_log.txt'):
    os.remove('baojianhui_log.txt') #删除之前的log
while not guizhang_flag:
    try:
        t.init()
        guizhang_flag = main(url=guizhang_url, mode = 'txt')
        t.close()
    except Exception as e:
        traceback.print_exc()
        # print("i am wrong")
        t.close()
if os.path.exists('baojianhui_log.txt'):
    os.remove('baojianhui_log.txt') #运行成功之后删除log
os.chdir('C:/Users/Administrator/Desktop')
s3_function.zip_ya('baojian_guizhang')
s3_function.upload_to_aws_s3('baojian_guizhang.zip','storageforccbrpa','baojian_guizhang_history.zip')

# os.chdir('/Users/maoyuanq/Desktop')
# os.mkdir('baojian_falv')
# os.chdir('/Users/maoyuanq/Desktop/baojian_falv')
# falv_flag = False
# falv_url = 'http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=927&itemUrl=ItemListRightList.html&itemName=法律法规&itemsubPId=926#'
# if os.path.exists('baojianhui_log.txt'):
#     os.remove('baojianhui_log.txt') #删除之前的log
# while not falv_flag:
#     try:
#         t.init()
#         falv_flag = main(url=falv_url, mode = 'txt')
#         t.close()
#     except Exception as e:
#         traceback.print_exc()
#         # print("i am wrong")
#         t.close()
# if os.path.exists('baojianhui_log.txt'):
#     os.remove('baojianhui_log.txt') #运行成功之后删除log
# os.chdir('/Users/maoyuanq/Desktop')
# s3_function.zip_ya('baojian_falv')
# s3_function.upload_to_aws_s3('baojian_falv.zip','storageforccbrpa','baojian_falv_history.zip')



#
# t.init()
# t.url('http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=927&itemUrl=ItemListRightList.html&itemName=法律法规&itemsubPId=926')
#
# t.wait(10)

#操作模块

#当前页面
# curr_page = int(t.read(element_identifier='//div[@class = "ng-binding"][last()]').split('/')[0])
# #点击按钮
# list_count = t.count(element_identifier='//div[@class = "list caidan-right-list"]') #循环列表，取出总list有几个
# for i in range(1, list_count+1):
#     t.wait(3)
#     item_count = t.count(
#         element_identifier='//div[@class = "list caidan-right-list"][' + str(i) + ']//div[@class = "panel-row ng-scope"]') #取出每个list里的具体法规有几条
#     print('当前是list {}, 里面的元素有 {} 个'.format(str(i),str(item_count)))
#     t.wait(3)
#     for j in range(1, item_count+1):
#         item_title = t.read(element_identifier='//div[@class = "list caidan-right-list"]['+str(i)+']//div[@class = "panel-row ng-scope"]['+str(j)+']//a')
#         time_suffix = t.read(element_identifier='//div[@class = "list caidan-right-list"]['+str(i)+']//div[@class = "panel-row ng-scope"]['+str(j)+']//span[@class = "date ng-binding"]')
#         file_name = item_title + '_' + time_suffix + '.txt'
#
#
#         #返回主页面
#         t.url('http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=927&itemUrl=ItemListRightList.html&itemName=法律法规&itemsubPId=926#'+str(curr_page))
#         t.wait(2)


#取txt模块
# #点击
# link = t.read(element_identifier='//div[@class = "list caidan-right-list"]['+str(i)+']//div[@class = "panel-row ng-scope"]['+str(j)+']//a/@ng-href')
# prefix = 'http://www.cbirc.gov.cn/cn/view/pages/'
# final_link = prefix + link
# t.url(final_link)
# while not os.path.exists(file_name):
#     content = t.read(element_identifier='//div[@class = "Section0"]')
#     with open(file_name,'w') as f:
#         f.write(content)

#翻页模块
# curr_page = int(t.read(element_identifier='//div[@class = "ng-binding"][last()]').split('/')[0])
# total_page = int(t.read(element_identifier='//div[@class = "ng-binding"][last()]').split('/')[-1])
# while curr_page < total_page: #从1开始，做完之后翻页；
#     print('click once')
#     t.click(element_identifier='//a[@ng-click = "pager.next()"]')

#取word版本
# t.click(element_identifier='//div[@class = "list caidan-right-list"][' + str(
#     i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a[@ng-click = "fileDownload(x.docFileUrl)"]')
# doc_id = t.read(element_identifier='//div[@class = "list caidan-right-list"][' + str(
#     i) + ']//div[@class = "panel-row ng-scope"][' + str(j) + ']//a/@ng-href').split('=')[1][:-7]
# doc_name = doc_id + '.doc'
# MAX = 30
# curr_clock = 5
# while not os.path.exists(file_name):
#     t.wait(curr_clock)
#     curr_clock += 5
#     if curr_clock > MAX:
#         break
# t.wait(2)
# os.rename(doc_name, item_title + '_' + time_suffix + '.doc')

